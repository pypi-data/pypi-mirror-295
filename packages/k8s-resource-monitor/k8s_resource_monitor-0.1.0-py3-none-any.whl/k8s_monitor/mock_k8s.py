from unittest import mock

def mock_kubernetes_api():
    """
    Simulates Kubernetes API responses for testing.
    """
    mock_v1 = mock.MagicMock()

    # Debugging: Print a message to confirm mock API is being used
    print("Mock Kubernetes API is being used")

    # Simulate response for list_namespaced_pod
    mock_v1.list_namespaced_pod.return_value = mock.Mock(
        items=[
            mock.Mock(
                metadata=mock.Mock(name="mock-pod-1"),
                status=mock.Mock(phase="Running"),
            ),
            mock.Mock(
                metadata=mock.Mock(name="mock-pod-2"),
                status=mock.Mock(phase="Pending"),
            ),
        ]
    )

    return mock_v1
