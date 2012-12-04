#! /usr/bin/env python

from setuptools import setup
import py2exe

setup(name="GameOfLife", 
      version="0.1", 
      author="Sreejith Kesavan", 
      author_email="sreejithemk@gmail.com", 
      url="https://github.com/semk/GameOfLife", 
      license="FreeBSD License", 
      packages=['gol'], 
      #package_data={"gol": ["ui/*"]}, 
      #scripts=["bin/liftr"], 
      windows=[{"script": "gol/gol.py"}], 
      options={"py2exe": {"skip_archive": True, 
                          "includes": ["sip"]}})
