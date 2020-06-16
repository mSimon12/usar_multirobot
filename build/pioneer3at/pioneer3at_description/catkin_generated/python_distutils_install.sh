#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/src/pioneer3at/pioneer3at_description"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/install/lib/python2.7/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/install/lib/python2.7/dist-packages:/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/build/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/build" \
    "/usr/bin/python2" \
    "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/src/pioneer3at/pioneer3at_description/setup.py" \
     \
    build --build-base "/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/build/pioneer3at/pioneer3at_description" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/install" --install-scripts="/media/marcelo/ARQUIVOS/desenvolvimento/projetos/usar_multirobot/install/bin"
