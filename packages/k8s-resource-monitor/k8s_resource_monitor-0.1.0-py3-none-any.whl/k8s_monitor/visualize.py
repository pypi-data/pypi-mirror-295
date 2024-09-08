import matplotlib.pyplot as plt
import datetime

def plot_resource_trends(cpu_usage_history, memory_usage_history, pod_name):
    """
    Plot CPU and memory usage trends for a specific pod.
    :param cpu_usage_history: List of CPU usage percentages.
    :param memory_usage_history: List of memory usage in MiB.
    :param pod_name: Name of the pod being visualized.
    """
    timestamps = [datetime.datetime.now() - datetime.timedelta(minutes=i * 10) for i in range(len(cpu_usage_history))]

    # Reverse the timestamps to plot correctly
    timestamps.reverse()
    cpu_usage_history.reverse()
    memory_usage_history.reverse()

    plt.figure(figsize=(12, 6))

    # Plot CPU usage trend
    plt.subplot(1, 2, 1)
    plt.plot(timestamps, cpu_usage_history, label="CPU Usage (%)", color='b')
    plt.fill_between(timestamps, cpu_usage_history, color='blue', alpha=0.1)
    plt.xlabel("Time")
    plt.ylabel("CPU Usage (%)")
    plt.title(f"CPU Usage Trend for Pod: {pod_name}")
    plt.xticks(rotation=45)
    plt.grid(True)

    # Plot Memory usage trend
    plt.subplot(1, 2, 2)
    plt.plot(timestamps, memory_usage_history, label="Memory Usage (Mi)", color='g')
    plt.fill_between(timestamps, memory_usage_history, color='green', alpha=0.1)
    plt.xlabel("Time")
    plt.ylabel("Memory Usage (Mi)")
    plt.title(f"Memory Usage Trend for Pod: {pod_name}")
    plt.xticks(rotation=45)
    plt.grid(True)

    plt.tight_layout()
    plt.show()
