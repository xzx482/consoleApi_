import traceback

from traceback import (
    __all__,
    _RECURSIVE_CUTOFF
    
)


_cause_message = (
    "\n以上异常导致了以下异常:\n\n")
_context_message = (
    "\n在处理以上异常的过程中, 又发生了另一个异常:\n\n")

def _some_str(value):
    try:
        return str(value)
    except:
        return '<无法打印的 %s 对象>' % type(value).__name__

class FrameSummary(traceback.FrameSummary):
    def __repr__(self):
        return "<帧摘要文件 {filename}, 在 {name} 中, 第 {lineno} 行>".format(
            filename=self.filename, name=self.name, lineno=self.lineno)

class StackSummary(traceback.StackSummary):
    def format(self):
        result = []
        last_file = None
        last_line = None
        last_name = None
        count = 0
        for frame in self:
            if (last_file is None or last_file != frame.filename or
                last_line is None or last_line != frame.lineno or
                last_name is None or last_name != frame.name):
                if count > _RECURSIVE_CUTOFF:
                    count -= _RECURSIVE_CUTOFF
                    result.append(
                        f'  [上一行重复了 {count} 次]\n'
                    )
                last_file = frame.filename
                last_line = frame.lineno
                last_name = frame.name
                count = 0
            count += 1
            if count > _RECURSIVE_CUTOFF:
                continue
            row = []
            row.append('  文件 "{}", 在 {} 中, 第 {} 行\n'.format(
                frame.filename, frame.name, frame.lineno))
            if frame.line:
                row.append('    {}\n'.format(frame.line.strip()))
            if frame.locals:
                for name, value in sorted(frame.locals.items()):
                    row.append('    {name} = {value}\n'.format(name=name, value=value))
            result.append(''.join(row))
        if count > _RECURSIVE_CUTOFF:
            count -= _RECURSIVE_CUTOFF
            result.append(
                f'  [上一行重复了 {count} 次]\n'
            )
        return result

class TracebackException(traceback.TracebackException):
    def _format_syntax_error(self, stype):
        filename_suffix = ''
        if self.lineno is not None:
            yield '  文件 "{}", 第 {} 行\n'.format(
                self.filename or "<string>", self.lineno)
        elif self.filename is not None:
            filename_suffix = ' ({})'.format(self.filename)

        text = self.text
        if text is not None:
            rtext = text.rstrip('\n')
            ltext = rtext.lstrip(' \n\f')
            spaces = len(rtext) - len(ltext)
            yield '    {}\n'.format(ltext)
            caret = (self.offset or 0) - 1 - spaces
            if caret >= 0:
                caretspace = ((c if c.isspace() else ' ') for c in ltext[:caret])
                yield '    {}^\n'.format(''.join(caretspace))
        msg = self.msg or "<无详细信息>"
        yield "{}: {}{}\n".format(stype, msg, filename_suffix)

    def format(self, *, chain=True):
        if chain:
            if self.__cause__ is not None:
                yield from self.__cause__.format(chain=chain)
                yield _cause_message
            elif (self.__context__ is not None and
                not self.__suppress_context__):
                yield from self.__context__.format(chain=chain)
                yield _context_message
            if self._truncated:
                yield (
                    '以下将导致回溯堆栈溢出的链式异常已被截断\n')
        if self.stack:
            yield '回溯 (最近一次调用):\n'
            yield from self.stack.format()
        yield from self.format_exception_only()
