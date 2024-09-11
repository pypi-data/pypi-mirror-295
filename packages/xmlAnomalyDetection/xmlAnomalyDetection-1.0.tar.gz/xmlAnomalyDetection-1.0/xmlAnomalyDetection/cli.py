# xmlAnomalyDetection/cli.py
import sys
from xmlAnomalyDetection.app import main

def main():
    main(sys.argv[1:])

if __name__ == "__main__":
    main()
