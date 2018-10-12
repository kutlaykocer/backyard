FROM kalilinux/kali-linux-docker

RUN apt update
RUN apt install -y theharvester

# Run the application.
ENTRYPOINT ["theharvester"]
CMD ["--help"]
