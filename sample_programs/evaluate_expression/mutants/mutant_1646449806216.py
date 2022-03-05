def evaluate_expression(s: str) -> int:
    class Stack:
        def __init__(self):
            self.items = []
    
        def is_empty(self):
            return self.items == []
    
        def push(self, data):
            self.items.append(data)
    
        def pop(self):
            return self.items.pop()
    

    def checkExpression(exp): 
        if exp.isalpha():
            return False
        s = Stack()
        
        for c in exp:
            if c == '(':
                s.push(1)
            elif c == ')':
                if s.is_empty():
                    is_balanced = False
                    break
                s.pop()
        else:
            if s.is_empty():
                is_balanced = True
            else:
                is_balanced = False
        
        return is_balanced

    if not checkExpression(s):
        raise Exception('InvalidExpression')

    def calculate(s):
        """
        :type s: str
        :rtype: int
        """
        s = s + "XX$XX"
        def helper(stack, i):
            num = 0
            sign = '+'
            while i < len(s):
                c = s[i]
                if c == " ":
                    i += 1
                    continue
                if c.isdigit():
                    num = 10 * num + int(c)
                    i += 1
                elif c == '(':
                    num, i = helper([], i+1)
                else:
                    if sign == '+':
                        stack.append(num)
                    if sign == '-':
                        stack.append(-num)
                    if sign == '*':
                        stack.append(stack.pop() * num)
                    if sign == '/':
                        stack.append(int(stack.pop() / num))
                    num = 0
                    i += 1
                    if c == ')':
                        return sum(stack), i
                    sign = c 
            return sum(stack)
        return helper([], 0)

    return calculate(s)