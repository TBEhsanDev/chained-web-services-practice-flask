#!/bin/bash
<<<<<<< HEAD
if [ -d "./venv" ]; then
	sudo rm -rf "./venv";
fi

=======
>>>>>>> 415335ff9f5bea62583bf450a49bb0656e5b4625
python3 -m venv venv && source "./venv/bin/activate" && pip install -r requirements
