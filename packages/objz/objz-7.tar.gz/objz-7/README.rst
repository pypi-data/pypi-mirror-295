README
######

NAME

::

    OBJZ - objects zen


SYNOPSIS

::

    objz  <cmd> [key=val] [key==val]


INSTALL

::

    $ pipx install objz
    $ pipx ensurepath


DESCRIPTION

::

    OBJZ has all you need to program a unix cli program, such as disk
    perisistence for configuration files, event handler to handle the
    client/server connection, code to introspect modules for
    commands, deferred exception handling to not crash on an error, a
    parser to parse commandline options and values, etc.

    OBJZ is Public Domain.


USAGE

::

    without any argument the program does nothing

    $ objz
    $

    see list of commands

    $ objz cmd
    cmd,err,mod,req,thr,ver

    list of modules

    $ objz mod
    cmd,err,fnd,irc,log,mod,req,rss,tdo,thr

    use -c to start a console

    $ objz -c

    use mod=<name1,name2> to load additional modules

    $ objz -c mod=irc,rss
    >


FILES

::

    ~/.objz
    ~/.local/bin/objz
    ~/.local/pipx/venvs/objz/

AUTHOR

::

    Bart Thate <rssbotd@gmail.com>


COPYRIGHT

::

    OBJZ is Public Domain.
