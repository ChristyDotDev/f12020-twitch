import socket

from f1_2020_telemetry.packets import unpack_udp_packet, PacketParticipantsData_V1, PacketLapData_V1

participants = {}
standings = {}


def get_standings():
    return standings


def run_telemetry():
    udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    udp_socket.bind(("", 20777))

    while True:
        udp_packet = udp_socket.recv(2048)
        packet = unpack_udp_packet(udp_packet)
        # print("Received:", packet)
        if len(participants.keys()) == 0 and isinstance(packet, PacketParticipantsData_V1):
            for i in range(0, int(packet.numActiveCars)):
                # ParticipantData_V1(aiControlled=1, driverId=49, teamId=71, raceNumber=9, nationality=10, name=b'AITKEN', yourTelemetry=1)
                participants[i] = packet.participants[i]
        # print(f"Participants: {participants}")

        if isinstance(packet, PacketLapData_V1):
            for i in range(0, len(participants)):
                # LapData_V1(lastLapTime=0.0, currentLapTime=105.1422119140625, sector1TimeInMS=48259, sector2TimeInMS=29117, bestLapTime=0.0, bestLapNum=0, bestLapSector1TimeInMS=0,
                # bestLapSector2TimeInMS=0, bestLapSector3TimeInMS=0, bestOverallSector1TimeInMS=48259, bestOverallSector1LapNum=1, bestOverallSector2TimeInMS=29117,
                # bestOverallSector2LapNum=1, bestOverallSector3TimeInMS=0, bestOverallSector3LapNum=0, lapDistance=4600.61572265625, totalDistance=4600.61572265625,
                # safetyCarDelta=-0.0, carPosition=18, currentLapNum=1, pitStatus=0, sector=2, currentLapInvalid=0, penalties=0, gridPosition=20, driverStatus=4, resultStatus=2)
                lap_data = packet.lapData[i]
                #print(participants[i].name.decode('utf-8'))
                standings_entry = {"driver": participants[i], "lapData": lap_data}
                standings[lap_data.carPosition] = standings_entry

        if len(standings) > 0:
            print(standings[1])

#TODO - create a bot user so I don't use my own