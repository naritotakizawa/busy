from busy import main
from busy import simple

if __name__ == '__main__':
    import sys
    app_name = sys.argv[1]
    if app_name == 'busy':
        main.main()
    elif app_name == 'busy-simple':
        simple.main()
    else:
        main.main()