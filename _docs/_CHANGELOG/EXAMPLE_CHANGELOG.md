[README repo](../../README.md) | [_docs](../README.md) | [_CHANGELOG](./README.md)

> Przykladowy format wpisu changelogu. Realne wpisy w tym repo musza wymieniac wszystkie zakonczone ID taskow i subtaskow.

# Filename: 1-2025-11-22-project-init-and-rpc.md

# 1. Project Initialization and Core RPC -> internal changelog title

**Date:** 2025-11-22  
**Version:** 0.1.0  
**Tasks:** TASK-001, TASK-002

## 🚀 Key Changes

### Core & Structure
- Initialized project using **Poetry**.
- Created directory structure compliant with **Clean Architecture** (`domain`, `application`, `adapters`, `infrastructure`).
- Configured `.gitignore` and development environment.

### Blender Addon (Server Side)
- Implemented **RPC Server** (`blender_addon/rpc_server.py`) running on TCP sockets (default port 8765).
- Used multi-threading model (`threading`) for network handling.
- Secured `bpy` API calls using `bpy.app.timers` to ensure Thread Safety.
- Added "Mock" mode support (running outside Blender).

### MCP Server (Client Side)
- Implemented **RPC Client** (`server/adapters/rpc/client.py`).
- Defined **Pydantic** communication models (`RpcRequest`, `RpcResponse`).
- Added automatic reconnection mechanisms and timeout handling.

### Testing
- Created integration test `tests/test_rpc_connection.py` verifying "Ping-Pong" communication.
