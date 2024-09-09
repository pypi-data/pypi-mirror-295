import serial.tools.list_ports
from wiliot_testers.test_equipment import Attenuator


def configure_attenuators_with_user_values():
    # List of possible attenuator types
    attn_types = ['MCDI-USB', 'MCDI', 'API', 'Weinschel']
    configured_devices = []

    for attn_type in attn_types:
        try:
            atten = Attenuator(attn_type)
            active_te = atten.GetActiveTE()
            configured_devices.append((attn_type, active_te))
            print(f"Detected and ready to configure {attn_type}.")
        except Exception as e:
            print(e)

    if not configured_devices:
        print("Unable to configure any device. Please check the connections.")
        return

    for device in configured_devices:
        attn_type, active_te = device
        try:
            value = float(input(f"Enter attenuation value for {attn_type}: "))
            active_te.Setattn(value)
            print(f"Successfully configured {attn_type} with attenuation {value}.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
        except Exception as e:
            print(f"Failed to set attenuation for {attn_type}: {e}")


if __name__ == "__main__":
    configure_attenuators_with_user_values()
