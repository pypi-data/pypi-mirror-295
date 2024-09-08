import logging
from rich.console import Console
from rich.table import Table
from k8s_monitor.mock_k8s import mock_kubernetes_api
from k8s_monitor.storage.database import init_db, log_pod_usage, get_average_usage, get_historical_usage
from k8s_monitor.utils.email_alerts import send_email_alert
from k8s_monitor.config import load_config
from k8s_monitor.autoscaling_policy import load_autoscaling_policy
from k8s_monitor.namespace_config import load_namespaces
import requests
from kubernetes import client, config as kube_config
from kubernetes.client import V2HorizontalPodAutoscaler, V2HorizontalPodAutoscalerSpec, V1CrossVersionObjectReference
from kubernetes.client import V2ResourceMetricSource, V2MetricSpec

# Configure logging
logging.basicConfig(filename='monitor.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

console = Console()

# Monitor resources in real-time
def monitor_resources(namespace=None, use_mock=False, minutes=10):
    try:
        if not namespace:
            namespaces = load_namespaces().get("namespaces", ["default"])
        else:
            namespaces = [namespace]

        console.print(f"Monitoring namespaces: [bold cyan]{', '.join(namespaces)}[/bold cyan]")
        init_db()

        for ns in namespaces:
            console.print(f"Fetching pods from namespace: {ns}")
            monitor_namespace(ns, use_mock, minutes)

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


def monitor_namespace(namespace, use_mock, minutes=10):
    config = load_config()
    if use_mock:
        console.print("[green]Using mock Kubernetes API[/green]")
        v1 = mock_kubernetes_api()
    else:
        console.print("[green]Using real Kubernetes API[/green]")
        kube_config.load_kube_config()
        v1 = client.CoreV1Api()

    pods = v1.list_namespaced_pod(namespace=namespace)
    console.print(f"Fetched {len(pods.items)} pods in namespace: {namespace}")

    if not pods.items:
        console.print(f"[red]No pods found in namespace: {namespace}[/red]")
        return

    pod_metrics = get_pod_metrics(namespace)
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Pod Name", style="dim")
    table.add_column("Phase")
    table.add_column("CPU Usage (%)")
    table.add_column("Memory Usage (Mi)")
    table.add_column("Historical CPU Usage (%)")
    table.add_column("Historical Memory Usage (Mi)")

    for pod in pods.items:
        pod_name = str(pod.metadata.name)
        phase = str(pod.status.phase)

        console.print(f"[blue]Processing pod: {pod_name} with phase {phase} in namespace {namespace}[/blue]")

        if pod_name in pod_metrics:
            cpu_usage = pod_metrics[pod_name]['cpu']
            memory_usage = pod_metrics[pod_name]['memory']
        else:
            cpu_usage = "N/A"
            memory_usage = "N/A"

        log_pod_usage(pod_name, namespace, cpu_usage, memory_usage)
        history = get_historical_usage(pod_name, namespace)

        historical_cpu = [usage['cpu'] for usage in history]
        historical_memory = [usage['memory'] for usage in history]

        table.add_row(
            pod_name, phase,
            str(cpu_usage), str(memory_usage),
            ", ".join(map(str, historical_cpu)),
            ", ".join(map(str, historical_memory))
        )

    console.print(table)

def configure_hpa(namespace, deployment_name, target_cpu_utilization_percentage=60, target_memory_utilization_percentage=None):
    """
    Configure or update the HPA for a given deployment.
    """
    kube_config.load_kube_config()
    v1_autoscaling = client.AutoscalingV2Api()

    hpa_name = f"{deployment_name}-hpa"
    
    try:
        # Check if the HPA already exists
        hpa = v1_autoscaling.read_namespaced_horizontal_pod_autoscaler(hpa_name, namespace)
        console.print(f"[yellow]HPA {hpa_name} already exists. Modifying...[/yellow]")
    except client.exceptions.ApiException as e:
        if e.status == 404:
            console.print(f"[green]Creating new HPA: {hpa_name}[/green]")
            hpa = None
        else:
            raise

    # Define CPU scaling policy
    metrics = [V2MetricSpec(
        type="Resource",
        resource=V2ResourceMetricSource(name="cpu", target_average_utilization=target_cpu_utilization_percentage)
    )]

    # Optionally add memory scaling policy
    if target_memory_utilization_percentage:
        metrics.append(V2MetricSpec(
            type="Resource",
            resource=V2ResourceMetricSource(name="memory", target_average_utilization=target_memory_utilization_percentage)
        ))

    # Create the HPA specification
    hpa_spec = V2HorizontalPodAutoscalerSpec(
        scale_target_ref=V1CrossVersionObjectReference(
            api_version="apps/v1",
            kind="Deployment",
            name=deployment_name,
        ),
        min_replicas=1,
        max_replicas=10,  # Can be configured
        metrics=metrics
    )

    # Either create or update the HPA
    if not hpa:
        hpa_body = V2HorizontalPodAutoscaler(
            metadata={'name': hpa_name, 'namespace': namespace},
            spec=hpa_spec
        )
        v1_autoscaling.create_namespaced_horizontal_pod_autoscaler(namespace, hpa_body)
    else:
        hpa.spec = hpa_spec
        v1_autoscaling.replace_namespaced_horizontal_pod_autoscaler(hpa_name, namespace, hpa)
    
    console.print(f"[green]HPA {hpa_name} configured successfully.[/green]")


# Auto-scale based on HPA logic
def auto_scale(namespace=None, use_mock=False):
    try:
        if not namespace:
            namespaces = load_namespaces().get("namespaces", ["default"])
        else:
            namespaces = [namespace]

        console.print(f"Auto-scaling namespaces: [bold cyan]{', '.join(namespaces)}[/bold cyan]")
        init_db()

        for ns in namespaces:
            console.print(f"Auto-scaling analysis for namespace: {ns}")
            auto_scale_namespace(ns, use_mock)

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


def auto_scale_namespace(namespace, use_mock):
    scaling_policy = load_autoscaling_policy()

    if use_mock:
        console.print("[green]Using mock Kubernetes API[/green]")
        v1 = mock_kubernetes_api()
    else:
        console.print("[green]Using real Kubernetes API[/green]")
        kube_config.load_kube_config()
        v1 = client.CoreV1Api()

    pods = v1.list_namespaced_pod(namespace=namespace)
    console.print(f"Fetched {len(pods.items)} pods in namespace: {namespace}")

    if not pods.items:
        console.print(f"[red]No pods found in namespace: {namespace}[/red]")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Pod Name", style="dim")
    table.add_column("Scaling Recommendation")

    for pod in pods.items:
        pod_name = str(pod.metadata.name)

        avg_cpu, avg_memory = get_average_usage(pod_name, namespace, 10)
        history = get_historical_usage(pod_name, namespace)

        recommendation = get_scaling_recommendation(avg_cpu, avg_memory, scaling_policy, history=history)

        # Add the data to the table
        table.add_row(pod_name, recommendation)

        # Call HPA function to apply autoscaling based on the recommendation
        if recommendation.startswith("Scale Up"):
            configure_hpa(namespace, pod_name, target_cpu_utilization_percentage=80)
        elif recommendation.startswith("Scale Down"):
            configure_hpa(namespace, pod_name, target_cpu_utilization_percentage=30)

    console.print(table)



def get_pod_metrics(namespace):
    try:
        api_instance = client.CustomObjectsApi()
        metrics = api_instance.list_namespaced_custom_object(
            group="metrics.k8s.io",
            version="v1beta1",
            namespace=namespace,
            plural="pods"
        )

        pod_metrics = {}
        for pod in metrics['items']:
            pod_name = pod['metadata']['name']
            cpu_usage = pod['containers'][0]['usage']['cpu']
            memory_usage = pod['containers'][0]['usage']['memory']
            pod_metrics[pod_name] = {
                "cpu": cpu_usage,
                "memory": memory_usage
            }

        return pod_metrics

    except Exception as e:
        console.print(f"[red]Error fetching pod metrics: {e}[/red]")
        return {}


def get_scaling_recommendation(avg_cpu, avg_memory, scaling_policy, history=None):
    target_cpu = scaling_policy.get("cpu_threshold", 60)
    target_memory = scaling_policy.get("memory_threshold", 60)
    max_replicas_change = scaling_policy.get("max_replicas_change", 5)

    recommendation = "No Scaling Needed"

    if avg_cpu is None or avg_memory is None:
        return recommendation

    avg_cpu = float(avg_cpu)
    avg_memory = float(avg_memory)

    if avg_cpu == 0 and avg_memory == 0:
        return "No Scaling Needed"

    if history:
        avg_cpu_trend = sum([usage['cpu'] for usage in history]) / len(history)
        avg_memory_trend = sum([usage['memory'] for usage in history]) / len(history)

        if avg_cpu_trend > target_cpu or avg_memory_trend > target_memory:
            scale_up_by = min(max_replicas_change, max(1, int((avg_cpu_trend - target_cpu) / 10)))
            recommendation = f"Scale Up by {scale_up_by} replicas due to usage trend"
        elif avg_cpu_trend < target_cpu and avg_memory_trend < target_memory:
            scale_down_by = min(max_replicas_change, max(0, int((target_cpu - avg_cpu_trend) / 10)))
            recommendation = f"Scale Down by {scale_down_by} replicas due to usage trend"

    return recommendation


# Alert logic remains unchanged from your original code
def trigger_alerts(pod_name, avg_cpu, avg_memory, config, cpu_threshold=80, memory_threshold=75):
    alert_triggered = False
    email_subject = f"Alert: High Resource Usage on {pod_name}"
    alert_message = ""

    if avg_cpu > cpu_threshold:
        console.print(f"[bold red]ALERT: High CPU usage on {pod_name}: {avg_cpu}% (Threshold: {cpu_threshold}%) [/bold red]")
        alert_message += f"CPU usage on {pod_name} is at {avg_cpu}% (Threshold: {cpu_threshold}%)\n"
        logging.info(f"High CPU usage on {pod_name}: {avg_cpu}%")
        alert_triggered = True

    memory_usage_mib = avg_memory / 1024
    if memory_usage_mib > memory_threshold:
        console.print(f"[bold red]ALERT: High Memory usage on {pod_name}: {memory_usage_mib}Mi (Threshold: {memory_threshold}Mi) [/bold red]")
        alert_message += f"Memory usage on {pod_name} is at {memory_usage_mib}Mi (Threshold: {memory_threshold}Mi)\n"
        logging.info(f"High Memory usage on {pod_name}: {memory_usage_mib}Mi")
        alert_triggered = True

    if alert_triggered:
        if "email_host" in config and "recipient_email" in config:
            send_email_alert(email_subject, alert_message)
            logging.info(f"Email alert sent for {pod_name}")
        else:
            console.print(f"[yellow]Email settings are not configured. Skipping email alerts.[/yellow]")

        if "slack_webhook_url" in config:
            send_slack_alert(config["slack_webhook_url"], alert_message)
            logging.info(f"Slack alert sent for {pod_name}")
        else:
            console.print(f"[yellow]Slack Webhook URL is not configured. Skipping Slack alerts.[/yellow]")


def send_slack_alert(slack_webhook_url, message):
    try:
        payload = {"text": message}
        response = requests.post(slack_webhook_url, json=payload)
        if response.status_code == 200:
            console.print("[green]Slack alert sent successfully.[/green]")
        else:
            console.print(f"[red]Failed to send Slack alert: {response.status_code}[/red]")
    except Exception as e:
        console.print(f"[red]Error sending Slack alert: {e}[/red]")
