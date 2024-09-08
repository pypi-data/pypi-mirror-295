import osirix
from osirix.dcm_pix import DCMPix
from osirix.viewer_controller import ViewerController
import grpc

from pyosirix_example.grpc_protocols import server_pb2_grpc
from pyosirix_example.grpc_protocols import server_pb2

class Client:
    """ Burn text to images on an OsiriX viewer controller.
    """
    def write_text_in_pix(self, text: str, pix: DCMPix) -> None:
        """ Write a text string in an OsiriX DCMPix instance.

        Args:
            text (str): The desired string.
            pix (DCMPix): The OsiriX DCMPix.
        """


    def write_text_in_viewer_controller(self, text: str, viewer: ViewerController,
                                        movie_idx: int = -1) -> None:
        """ Write a text string in all DCMPix instances within a viewer.

        Args:
            text (str): The desired string.
            viewer (ViewerController): The OsiriX ViewerController.
            movie_idx (int): The frame of the viewer in which to write the text. Default is -1 in
                which case all frames are written.
        """
        if movie_idx == -1:
            for idx in range(viewer.max_movie_index):
                pix_list = viewer.pix_list(idx)
                for pix in pix_list:
                    self.write_text_in_pix(text, pix)
        else:
            pix_list = viewer.pix_list(movie_idx)
            for pix in pix_list:
                self.write_text_in_pix(text, pix)
        viewer.needs_display_update()

    def write_text_in_selected_viewer_controller(self) -> None:
        """ Write a text string in all DCMPix instances within the user-selected viewer.
        """
        viewer = osirix.frontmost_viewer()

    def run(self):
        self.write_text_in_selected_viewer_controller()


def run():
    # Replace 'localhost' with the specific IP address of the server
    server_address = '192.168.1.100:50051'  # Replace with your server's IP address and port
    with grpc.insecure_channel(server_address) as channel:
        # Create a stub (client)
        stub = server_pb2_grpc.ServiceStub(channel)

        # Create a sample request with an array of image data
        rows, columns = 2, 3  # Example dimensions
        image_data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]  # Example image data

        request = server_pb2.Image(rows=rows, columns=columns, image=image_data)
        print(f"Sending Image: {rows}x{columns} with data {image_data}")

        # Call the ProcessImage method
        response = stub.ProcessImage(request)
        print(
            f"Received Processed Image: {response.rows}x{response.columns} with data {response.image}")


# How to run the client.
if __name__ == '__main__':
    # You could process arguments here.
    Client().run()
