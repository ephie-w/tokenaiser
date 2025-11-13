'''
Author: Yifei Wang
Github: ephiewangyf@gmail.com
Date: 2025-11-13
Description: Callback functions for ADK agents - Mock implementations (Optimized for compatibility)
'''
from typing import Any, Dict
from datetime import datetime

# 💡 解决方案 1：移除回调函数定义中的特定参数，只使用 **kwargs
# 这样可以兼容 ADK 传入的任何参数 (包括 callback_context, trace_id, 等)
def ops_tracing(**kwargs) -> Dict[str, Any]:
    """Operations tracing callback - called before agent execution."""
    
    # 打印 kwargs 来查看 ADK 实际传入了哪些参数
    # print("Agent execution context:", kwargs) 
    
    trace_id = f"trace_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
    print(f"[OPS_TRACING] {trace_id}")


def failure_alert(**kwargs) -> Dict[str, Any]:
    """Failure alert callback - called after agent execution."""
    
    # print("Agent execution context:", kwargs)

    # 从 kwargs 中安全地获取上下文信息，用于检查失败状态
    callback_context = kwargs.get("callback_context", {})
    
    has_failure = False
    failure_reason = None
    
    if isinstance(callback_context, dict):
        # 检查上下文中的错误信息
        if callback_context.get("error") or callback_context.get("status") == "error":
            has_failure = True
            failure_reason = callback_context.get("error") or callback_context.get("failure_reason", "Unknown error")
    
    if "error" in kwargs:
        has_failure = True
        failure_reason = str(kwargs.get("error"))
    
    # 假设 ADK 框架允许返回自定义数据，但不允许返回基本事件元数据
    if has_failure:
        return {
            "alert_sent": True,
            "alert_level": "error",
            "failure_reason": failure_reason, # 使用一个更自定义的键名
        }
    else:
        return {
            "alert_sent": False,
        }