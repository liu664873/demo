from browser import document as doc, window
import javascript
import sys
import traceback
import re

manager = window.manager

code_head = '''
player = manager.getPlayer()
ship = manager.getShip()
energy = manager.getEnergyList()
flyer = manager.getFlyerList()
print(flyer)
'''

code_tail = '''
manager.playActionAnims()
'''

class ProgramStepCountOverflowException(Exception):
    def __init__(self, errorInfo):
        Exception.__init__(self)
        self.errorInfo = errorInfo
    def __str__(self):
        return self.errorInfo

program_step_count = 0
        
def recordOneStep(lineNumber):
    global program_step_count
    program_step_count += 1
    if program_step_count > 5000:
        program_step_count = 0
        manager.editor.errorLine = lineNumber
        raise ProgramStepCountOverflowException('Program step exceed! Dead loop?')

def handleOneStep(lineNumber):
    recordOneStep(lineNumber)
    manager.editor.runLine = lineNumber

def getStartSpaceCount(s):
    return len(s) - len(s.lstrip())

def echo(event):
    error_str = ""
    manager.editor.errorLine = -1
    
    try:
        # 获取并预处理代码
        code = manager.editor.getValue()
        old_lines = [line.replace('\t', '    ') for line in code.split('\n')]
        
        # 生成有效的line_dict（跳过空行和注释）
        line_dict = []
        for i, line in enumerate(old_lines):
            line_stripped = line.strip()
            if not line_stripped or line_stripped.startswith('#'):
                continue
            line_dict.append([i + 1, line])  # [行号, 行内容]
        
        # 代码静态分析
        analysis_result = manager.editor.analysisPythonCode(line_dict)
        if analysis_result.error:
            raise Exception(analysis_result.error)
        
        # 生成带handleOneStep的新代码
        newLines = []
        for i, (line_num, line_content) in enumerate(line_dict):
            indent = ' ' * getStartSpaceCount(line_content)
            stripped = line_content.strip()
            
            # 检测是否为else/elif行
            is_control_flow = re.match(r'^\s*(else|elif)\s*:', stripped)
            
            # 非控制流行才插入handleOneStep
            if not is_control_flow:
                newLines.append(f"{indent}handleOneStep({line_num})")
            
            newLines.append(line_content)
        
        # 组合完整代码并执行
        full_code = code_head + '\n'.join(newLines) + code_tail
        exec(full_code)
        
    except SyntaxError as exc:
        # 计算错误行号（考虑code_head的行数偏移）
        error_line = max(1, int((exc.lineno - len(code_head.split('\n'))))
        manager.editor.errorLine = error_line
        err_message = manager.editor.session.getLine(error_line - 1)
        error_str = f'Error [Line {error_line}]: "{err_message}" 有语法错误，请仔细检查!'
        manager.showPrompt("错误", error_str, errorCallback1, errorCallback2)
        
    except Exception as exc:
        traceback.print_exc()
        error_str = f'Error [Line {manager.editor.errorLine}]: {str(exc)}'
        manager.showPrompt("错误", error_str, errorCallback1, errorCallback2)

def stop(event):
    if manager.actionAnims:
        manager.pauseActionAnims()
    else:
        manager.resumeActionAnims()
    
def new(event):
    manager.editor.removeAllHighlight()
    manager.showPrompt("重试", "是否重置场景", cancel, resetScene) 

def errorCallback1():
    manager.editor.removeHighlight()

def errorCallback2():
    manager.editor.removeHighlight()

def clear(event):
    manager.showPrompt("重试", "是否重置代码", cancel, resetCode) 

def resetScene():
    resetCode()
    manager.selectLevel(manager.curLevel)

def resetCode():
    manager.editor.editor.setValue('')

def cancel():
    pass

# 绑定事件
doc["run"].bind("click", echo)
doc["new"].bind("click", new)
doc["stop"].bind("click", stop)
doc["clear"].bind("click", clear)