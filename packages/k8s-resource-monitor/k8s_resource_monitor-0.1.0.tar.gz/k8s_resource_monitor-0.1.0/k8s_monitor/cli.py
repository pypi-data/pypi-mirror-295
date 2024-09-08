import click
from k8s_monitor.monitor import monitor_resources, auto_scale as auto_scale_command, get_historical_usage
from k8s_monitor.utils.email_alerts import send_email_alert
from k8s_monitor.config import load_config, save_config, view_config as view_current_config, reset_config as reset_current_config
from k8s_monitor.autoscaling_policy import load_autoscaling_policy, save_autoscaling_policy, view_autoscaling_policy as view_current_autoscaling_policy, reset_autoscaling_policy as reset_current_autoscaling_policy
from k8s_monitor.namespace_config import load_namespaces, save_namespaces, view_namespaces as view_current_namespaces, reset_namespaces as reset_current_namespaces
from k8s_monitor.visualize import plot_resource_trends
import os

@click.group()
def cli():
    """
    Kubernetes Resource Monitor CLI.
    """
    pass

@cli.command()
@click.option('--slack-webhook-url', help='Set Slack Webhook URL for alerts')
@click.option('--email-host', help='Set SMTP host for email alerts')
@click.option('--email-port', type=int, help='Set SMTP port for email alerts')
@click.option('--sender-email', help='Set the sender email address for alerts')
@click.option('--sender-password', help='Set the sender email password for alerts')
@click.option('--recipient-email', help='Set the recipient email address for alerts')
def set_config(slack_webhook_url, email_host, email_port, sender_email, sender_password, recipient_email):
    """
    Set configuration for the Kubernetes monitor (e.g., Slack webhook, email settings).
    """
    config = load_config()

    # Update config values if provided
    if slack_webhook_url:
        config['slack_webhook_url'] = slack_webhook_url
    if email_host:
        config['email_host'] = email_host
    if email_port:
        config['email_port'] = email_port
    if sender_email:
        config['sender_email'] = sender_email
    if sender_password:
        config['sender_password'] = sender_password
    if recipient_email:
        config['recipient_email'] = recipient_email

    save_config(config)
    print("Configuration updated successfully.")

# Config Commands
@cli.command()
def view_config():
    """
    View the current configuration.
    """
    view_current_config()

@cli.command()
def reset_config():
    """
    Reset the configuration to default (clear config file).
    """
    reset_current_config()

@cli.command()
@click.option('--cpu-threshold', type=int, help='Set the CPU usage threshold for auto-scaling')
@click.option('--memory-threshold', type=int, help='Set the memory usage threshold for auto-scaling')
@click.option('--max-replicas-change', type=int, help='Set the maximum number of replicas to scale up or down')
@click.option('--scaling-strategy', type=click.Choice(['static', 'dynamic']), help='Set the scaling strategy (static or dynamic)')
def set_autoscaling_policy(cpu_threshold, memory_threshold, max_replicas_change, scaling_strategy):
    """
    Set the auto-scaling policy for Kubernetes monitoring.
    """
    policy = load_autoscaling_policy()

    if cpu_threshold:
        policy['cpu_threshold'] = cpu_threshold
    if memory_threshold:
        policy['memory_threshold'] = memory_threshold
    if max_replicas_change:
        policy['max_replicas_change'] = max_replicas_change
    if scaling_strategy:
        policy['scaling_strategy'] = scaling_strategy

    save_autoscaling_policy(policy)
    print("Auto-scaling policy updated successfully.")

@cli.command()
def view_autoscaling_policy():
    """
    View the current auto-scaling policy.
    """
    view_current_autoscaling_policy()

@cli.command()
def reset_autoscaling_policy():
    """
    Reset the auto-scaling policy to default.
    """
    reset_current_autoscaling_policy()

@cli.command()
@click.option('--namespaces', multiple=True, help='Set the namespaces for cluster-wide monitoring (use space-separated values)')
def set_namespaces(namespaces):
    """
    Set namespaces for cluster-wide monitoring.
    """
    if not namespaces:
        print("No namespaces provided.")
        return

    namespace_config = {'namespaces': list(namespaces)}
    save_namespaces(namespace_config)
    print("Namespaces updated successfully.")


@cli.command()
def view_namespaces():
    """
    View the current namespaces being monitored.
    """
    view_current_namespaces()

@cli.command()
def reset_namespaces():
    """
    Reset the namespaces to the default.
    """
    reset_current_namespaces()

@cli.command()
@click.option('--namespace', default='default', help='Kubernetes namespace to monitor')
@click.option('--use-mock', is_flag=True, help='Use mock data instead of live Kubernetes cluster')
def monitor(namespace, use_mock):
    """
    Monitor real-time resource usage in a specific namespace.
    """
    try:
        print(f"Monitor command called with namespace={namespace}, use_mock={use_mock}")
        monitor_resources(namespace=namespace, use_mock=use_mock)
    except Exception as e:
        print(f"Error in monitor command: {e}")

@cli.command()
@click.option('--namespace', default='default', help='Kubernetes namespace to monitor')
@click.option('--use-mock', is_flag=True, help='Use mock data instead of live Kubernetes cluster')
def auto_scale(namespace, use_mock):
    """
    Provide auto-scaling recommendations based on the average usage in a given namespace.
    """
    try:
        print(f"Auto-scale command called with namespace={namespace}, use_mock={use_mock}")
        auto_scale_command(namespace=namespace, use_mock=use_mock)  # This will now refer to the auto-scaling logic
    except Exception as e:
        print(f"Error in auto_scale command: {e}")

@cli.command()
@click.option('--namespace', default='default', help='Kubernetes namespace to monitor')
@click.option('--pod-name', required=True, help='The name of the pod to visualize trends for')
@click.option('--duration', default=60, help='Time duration (in minutes) for historical data')
def visualize_trends(namespace, pod_name, duration):
    """
    Visualize resource trends for a specific pod over a specified duration.
    """
    try:
        history = get_historical_usage(pod_name, namespace, duration)
        
        if not history:
            print(f"No historical data available for pod {pod_name}.")
            return
        
        # Extract CPU and memory usage histories from the data
        cpu_usage_history = [entry['cpu'] for entry in history]
        memory_usage_history = [entry['memory'] for entry in history]

        # Ensure they are lists (in case of unexpected data types)
        if not isinstance(cpu_usage_history, list) or not isinstance(memory_usage_history, list):
            raise ValueError("CPU or memory usage history is not in list form")

        # Plot the trends
        plot_resource_trends(cpu_usage_history, memory_usage_history, pod_name)

    except Exception as e:
        print(f"Error visualizing trends: {e}")



@cli.command()
@click.option('--email-host', required=True, help='SMTP host for sending alerts')
@click.option('--email-port', required=True, help='SMTP port for sending alerts')
@click.option('--sender-email', required=True, help='Sender email for alerts')
@click.option('--sender-password', required=True, help='Sender password for alerts')
@click.option('--recipient-email', required=True, help='Recipient email for alerts')
@click.option('--subject', required=True, help='Subject of the email alert')
@click.option('--message', required=True, help='Message content of the email alert')
def email_alert(email_host, email_port, sender_email, sender_password, recipient_email, subject, message):
    """
    Send email alerts independently of monitoring.
    """
    try:
        print("Email alert command called")
        os.environ['EMAIL_HOST'] = email_host
        os.environ['EMAIL_PORT'] = str(email_port)
        os.environ['SENDER_EMAIL'] = sender_email
        os.environ['SENDER_PASSWORD'] = sender_password
        os.environ['RECIPIENT_EMAIL'] = recipient_email

        send_email_alert(subject, message)
        click.echo("Email alert sent.")
    except Exception as e:
        print(f"Error in email_alert command: {e}")

if __name__ == '__main__':
    cli()
