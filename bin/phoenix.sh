#!/bin/bash
# Manager for Phoenix System Monitor
SERVICE=phoenix
SERVICE_FILE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/phoenix.service"

function install_service() {
    echo "[INFO] Installing service..."
    sudo cp "$SERVICE_FILE" /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable $SERVICE
    echo "[INFO] Service installed and enabled."
}

function start_service() {
    echo "[INFO] Starting service..."
    sudo systemctl start $SERVICE
    sudo systemctl status $SERVICE --no-pager
}

function stop_service() {
    echo "[INFO] Stopping service..."
    sudo systemctl stop $SERVICE
}

function restart_service() {
    echo "[INFO] Restarting service..."
    sudo systemctl restart $SERVICE
    sudo systemctl status $SERVICE --no-pager
}

function remove_service() {
    echo "[INFO] Removing service..."
    sudo systemctl stop $SERVICE
    sudo systemctl disable $SERVICE
    sudo rm -f /etc/systemd/system/${SERVICE}.service
    sudo systemctl daemon-reload
    echo "[INFO] Service removed."
}

function status_service() {
    sudo systemctl status $SERVICE --no-pager
}

case "$1" in
    install)
        install_service
        ;;
    start)
        start_service
        ;;
    stop)
        stop_service
        ;;
    restart)
        restart_service
        ;;
    remove)
        remove_service
        ;;
    status)
        status_service
        ;;
    *)
        echo "Usage: $0 {install|start|stop|restart|remove|status}"
        exit 1
        ;;
esac
