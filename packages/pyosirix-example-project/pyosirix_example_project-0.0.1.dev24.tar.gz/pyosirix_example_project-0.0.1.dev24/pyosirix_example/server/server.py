from concurrent import futures

import grpc
import numpy as np

from data_loader import DataLoader
from pyosirix_example.grpc_protocols import server_pb2_grpc
from pyosirix_example.grpc_protocols import server_pb2
from pyosirix_example.utilities.text_2_image import Text2Image

class Service(server_pb2_grpc.ServiceServicer):
    def __init__(self):
        self.data_loader = DataLoader()

    def process(self, request):
        # Log the received image details
        print(
            f"Received Image: {request.rows}x{request.columns} with data size {len(request.image)}")

        # Convert to numpy array
        array = np.array(request.image).reshape(request.rows, request.columns)

        # Get the data to add
        text = self.data_loader.data

        # Process the image
        t2i = Text2Image()
        new_array = t2i.paste_text_in_array(text,
                                            array,
                                            location=3,  # Top left
                                            scale=0.75,
                                            offset=0.05,
                                            remove_background=False,
                                            align="left",
                                            font_path="GillSans.ttc",
                                            value=4095,
                                            bg_value=0)

        # Create a list
        flat_list = new_array.ravel().tolist()

        # Return the processed image
        return server_pb2.Image(rows=request.rows, columns=request.columns, image=flat_list)


def serve(ip_address: str = "127.0.0.1", port: int = 50051):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server_pb2_grpc.add_ServiceServicer_to_server(Service(), server)
    server.add_insecure_port(f'{ip_address}:{port}')
    server.start()
    print(f"Server is running on port {port}...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()