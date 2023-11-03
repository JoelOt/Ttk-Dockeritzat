# Ttk-Dockeritzat

He dockeritzat aquesta interficie grafica.

docker build -t pyttk:1 .
docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix pyttk:1

