import socket

from f1_2020_telemetry.packets import unpack_udp_packet, PacketParticipantsData_V1, PacketLapData_V1, \
    PacketCarStatusData_V1

player_car_index = {}
participants = {}
standings = {}
player_status = {}

tyre_compounds = {
    7: "Inter",
    8: "Wet",
    9: "Dry",
    10: "Wet",
    11: "Super Soft",
    12: "Soft",
    13: "Medium",
    14: "Hard",
    15: "Wet",
    16: "C5",
    17: "C4",
    18: "C3",
    19: "C2",
    20: "C1",
}


def get_standings():
    if len(standings) > 0:
        return standings
    return None


def get_player_status():
    return player_status[player_car_index[0]]


def run_telemetry():
    udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    udp_socket.bind(("", 20777))
    print("Listening to F1 telemetry")

    while True:
        udp_packet = udp_socket.recv(2048)
        packet = unpack_udp_packet(udp_packet)

        if len(participants.keys()) == 0 and isinstance(packet, PacketParticipantsData_V1):
            player_car_index[0] = packet.header.playerCarIndex
            for i in range(0, int(packet.numActiveCars)):
                participants[i] = packet.participants[i]

        if isinstance(packet, PacketLapData_V1):
            for i in range(0, len(participants)):
                lap_data = packet.lapData[i]
                standings_entry = {"driver": participants[i], "lapData": lap_data}
                standings[lap_data.carPosition] = standings_entry

        if isinstance(packet, PacketCarStatusData_V1):
            player_status[player_car_index[0]] = packet.carStatusData[player_car_index[0]]
