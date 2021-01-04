import socket

from f1_2020_telemetry.packets import unpack_udp_packet, PacketParticipantsData_V1, PacketLapData_V1

participants = {}
standings = {}


def get_standings():
    if len(standings) > 0:
        return standings
    return None


def run_telemetry():
    udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    udp_socket.bind(("", 20777))

    while True:
        udp_packet = udp_socket.recv(2048)
        packet = unpack_udp_packet(udp_packet)
        if len(participants.keys()) == 0 and isinstance(packet, PacketParticipantsData_V1):
            for i in range(0, int(packet.numActiveCars)):
                participants[i] = packet.participants[i]

        if isinstance(packet, PacketLapData_V1):
            for i in range(0, len(participants)):
                lap_data = packet.lapData[i]
                standings_entry = {"driver": participants[i], "lapData": lap_data}
                standings[lap_data.carPosition] = standings_entry
