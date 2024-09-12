from typing import Tuple, List
import numpy as np
import redis


class PhaseService:

    def __init__(self, client: redis.Redis):
        self.client = client

    async def batch_process_phase(self, data_batch: List[Tuple[int, bytes]], expiration_time: int):
        """
        batch process phase data
        :param data_batch: batch of Tuple (measurement_timestamp, phase data)
        :param expiration_time: expiration time of phase data ( seconds )
        :return: None
        """
        # Create a dictionary for zadd with timestamps as scores
        batch_data_dict = {phase_data: timestamp for timestamp, phase_data in data_batch}

        # Use pipeline to execute multiple commands in a batch
        with self.client.pipeline() as pipe:
            # Add multiple elements to the sorted set
            await pipe.zadd("phase", batch_data_dict)

            # Set expiration time for each element in the sorted set
            for timestamp, phase_data in data_batch:
                await pipe.expireat("phase", timestamp + expiration_time)

            # Execute all commands in the pipeline
            pipe.execute()

    async def get_phase(self, start_timestamp: int, end_timestamp: int) -> (int, np.ndarray):
        """
        get phase data from start_time to end_time
        :param start_timestamp: start time
        :param end_timestamp: end time
        :return: (begin_timestamp, phase data)
        """
        group_of_phase_data = await self.client.zrangebyscore("phase", start_timestamp, end_timestamp)  # List[key]
        start_of_phase_data = group_of_phase_data[0]
        start_timestamp_of_phase_data = await self.client.zscore("phase", start_of_phase_data)
        result_of_parsing_phase_data = []
        for phase_data_bytes in group_of_phase_data:
            phase_data = np.frombuffer(phase_data_bytes, dtype=np.int32)
            phase_data = phase_data.flatten()
            result_of_parsing_phase_data.append(phase_data)
        return start_timestamp_of_phase_data, np.array(result_of_parsing_phase_data)
