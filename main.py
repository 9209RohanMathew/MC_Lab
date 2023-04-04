import os
import socket
import streamlit as st

# Get the IP address of the server
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_address = s.getsockname()[0]
s.close()

def send_file(filename):
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set the socket timeout to 1 second
    sock.settimeout(1)

    # Get the broadcast address for the current network
    broadcast_address = '.'.join(ip_address.split('.')[:-1]) + '.255'

    # Send the filename to all devices on the network
    message = filename.encode('utf-8')
    sock.sendto(message, (broadcast_address, 12345))

    # Close the socket
    sock.close()

def main():
    st.title('File Sharing App')
    st.write(f'Your IP address is: {ip_address}')

    uploaded_file = st.file_uploader('Upload a file')
    if uploaded_file is not None:
        # Save the uploaded file to the server
        with open(os.path.join('uploads', uploaded_file.name), 'wb') as f:
            f.write(uploaded_file.getbuffer())

        # Send the filename to all devices on the network
        send_file(uploaded_file.name)

        st.success('File uploaded and shared successfully!')

if __name__ == '__main__':
    main()
