import psutil
import platform
import json
import inventoryos

def get_system_info():
    # Get system information
    system_info = {
        "System": platform.system(),
        "Release": platform.release(),
        "Version": platform.version(),
        "Architecture": platform.architecture()
    }

    # Get CPU usage
    cpu_usage = psutil.cpu_percent(interval=1, percpu=True)

    # Get memory usage
    memory = psutil.virtual_memory()

    # Get disk usage
    disk = psutil.disk_usage("/")

    # Get network interfaces and their statistics
    network = {}
    net_if_stats = psutil.net_if_stats()
    for interface, stats in net_if_stats.items():
        network[interface] = {
            "is_up": stats.isup,
            "duplex": stats.duplex,
            "speed": stats.speed,
            "mtu": stats.mtu
        }

    # Create the response JSON object
    response = {
        "SystemInfo": system_info,
        "CPUUsage": cpu_usage,
        "MemoryUsage": {
            "Total": memory.total,
            "Available": memory.available,
            "Used": memory.used,
            "PercentUsed": memory.percent
        },
        "DiskUsage": {
            "Total": disk.total,
            "Used": disk.used,
            "Free": disk.free,
            "PercentUsed": disk.percent
        },
        "NetworkInterfaces": network
    }

    return response

# Example usage
if __name__ == "__main__":
    system_info = get_system_info()
    print(json.dumps(system_info, indent=4))