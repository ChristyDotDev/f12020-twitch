import socket

from f1_2020_telemetry.packets import unpack_udp_packet, PacketParticipantsData_V1, PacketLapData_V1

participants = None

def main():
    udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    udp_socket.bind(("", 20777))

    while True:
        udp_packet = udp_socket.recv(2048)
        packet = unpack_udp_packet(udp_packet)
        # print("Received:", packet)
        if participants is None and isinstance(packet, PacketParticipantsData_V1):
            print(packet.numActiveCars)
            for participant in packet.participants:
                participants[participant.raceNumber] = participant
                #ParticipantData_V1(aiControlled=1, driverId=49, teamId=71, raceNumber=9, nationality=10, name=b'AITKEN', yourTelemetry=1)
                print(f'aiController:{participant.aiControlled}')
                print(f'name:{participant.name}')
                print(f'aiController:{participant.name}')

        if isinstance(packet, PacketLapData_V1):
            lap_data = packet.lapData
            print(len(lap_data))
            for car in lap_data:
                print(car.gridPosition)
            # LapData_V1(lastLapTime=120.56275177001953, currentLapTime=107.59722137451172, sector1TimeInMS=36266, sector2TimeInMS=28277, bestLapTime=120.56275177001953,
            # bestLapNum=1, bestLapSector1TimeInMS=47002, bestLapSector2TimeInMS=28902, bestLapSector3TimeInMS=44657, bestOverallSector1TimeInMS=36266,
            # bestOverallSector1LapNum=2, bestOverallSector2TimeInMS=28277, bestOverallSector2LapNum=2, bestOverallSector3TimeInMS=44657, bestOverallSector3LapNum=1,
            # lapDistance=5240.943359375, totalDistance=10542.224609375, safetyCarDelta=-0.0, carPosition=20, currentLapNum=2, pitStatus=0, sector=2, currentLapInvalid=0,
            # penalties=0, gridPosition=20, driverStatus=4, resultStatus=2),


main()
