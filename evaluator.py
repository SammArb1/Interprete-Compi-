# EVALUADOR DEL AST (TREE-WALKER)

from ast_nodes import *
from objects import *
from environment import Environment

TRUE_OBJ = BooleanVal(True)
FALSE_OBJ = BooleanVal(False)
NULL_OBJ = Null()
BREAK_OBJ = BreakValue()

BUILTINS = {
    "len": Builtin(lambda *args: Integer(len(args[0].elements)) if len(args) == 1 and args[0].type() == ObjType.ARRAY else Error("argumento para 'len' no soportado")),
    "print": Builtin(lambda *args: print(*[a.inspect() for a in args]) or NULL_OBJ)
}

def is_error(obj):
    return obj is not None and obj.type() == ObjType.ERROR

def native_bool_to_bool_object(input_val):
    return TRUE_OBJ if input_val else FALSE_OBJ

def evaluate(node, env):
    if isinstance(node, Program):
        return eval_program(node.statements, env)
    elif isinstance(node, BlockStatement):
        return eval_block_statement(node, env)
    elif isinstance(node, ExpressionStatement):
        return evaluate(node.expression, env)
    elif isinstance(node, ReturnStatement):
        val = evaluate(node.return_value, env)
        if is_error(val): return val
        return ReturnValue(val)
    elif isinstance(node, BreakStatement):
        return BREAK_OBJ
    elif isinstance(node, LetStatement):
        val = evaluate(node.value, env)
        if is_error(val): return val
        env.set(node.name.value, val)
        return val
    elif isinstance(node, AssignExpression):
        val = evaluate(node.value, env)
        if is_error(val): return val
        env.assign(node.name.value, val)
        return val
    elif isinstance(node, IntegerLiteral):
        return Integer(node.value)
    elif isinstance(node, StringLiteral):
        return StringObj(node.value)
    elif isinstance(node, Boolean):
        return native_bool_to_bool_object(node.value)
    elif isinstance(node, PrefixExpression):
        right = evaluate(node.right, env)
        if is_error(right): return right
        return eval_prefix_expression(node.operator, right)
    elif isinstance(node, InfixExpression):
        left = evaluate(node.left, env)
        if is_error(left): return left
        right = evaluate(node.right, env)
        if is_error(right): return right
        return eval_infix_expression(node.operator, left, right)
    elif isinstance(node, IfExpression):
        return eval_if_expression(node, env)
    elif isinstance(node, WhileExpression):
        return eval_while_expression(node, env)
    elif isinstance(node, ForExpression):
        return eval_for_expression(node, env)
    elif isinstance(node, Identifier):
        return eval_identifier(node, env)
    elif isinstance(node, FunctionLiteral):
        params = node.parameters
        body = node.body
        return FunctionObj(params, body, env)
    elif isinstance(node, CallExpression):
        function = evaluate(node.function, env)
        if is_error(function): return function
        args = eval_expressions(node.arguments, env)
        if len(args) == 1 and is_error(args[0]): return args[0]
        return apply_function(function, args)
    elif isinstance(node, ArrayLiteral):
        elements = eval_expressions(node.elements, env)
        if len(elements) == 1 and is_error(elements[0]): return elements[0]
        return ArrayObj(elements)
    elif isinstance(node, IndexExpression):
        left = evaluate(node.left, env)
        if is_error(left): return left
        index = evaluate(node.index, env)
        if is_error(index): return index
        return eval_index_expression(left, index)
    return None

def eval_program(stmts, env):
    result = None
    for stmt in stmts:
        result = evaluate(stmt, env)
        if isinstance(result, ReturnValue):
            return result.value
        elif isinstance(result, Error):
            return result
    return result

def eval_block_statement(block, env):
    result = None
    for stmt in block.statements:
        result = evaluate(stmt, env)
        if result is not None and (result.type() == ObjType.RETURN_VALUE or result.type() == ObjType.ERROR or result.type() == ObjType.BREAK_VALUE):
            return result
    return result

def eval_prefix_expression(operator, right):
    if operator == "!": return eval_bang_operator_expression(right)
    elif operator == "-": return eval_minus_prefix_operator_expression(right)
    return Error(f"operador desconocido: {operator}{right.type()}")

def eval_bang_operator_expression(right):
    if right == TRUE_OBJ or right != FALSE_OBJ and right != NULL_OBJ:
        return FALSE_OBJ
    return TRUE_OBJ

def eval_minus_prefix_operator_expression(right):
    if right.type() != ObjType.INTEGER:
        return Error(f"operador desconocido: -{right.type()}")
    return Integer(-right.value)

def eval_infix_expression(operator, left, right):
    if left.type() == ObjType.INTEGER and right.type() == ObjType.INTEGER:
        return eval_integer_infix_expression(operator, left, right)
    elif left.type() == ObjType.STRING and right.type() == ObjType.STRING:
        return eval_string_infix_expression(operator, left, right)
    elif operator == "==": return native_bool_to_bool_object(left == right)
    elif operator == "!=": return native_bool_to_bool_object(left != right)
    elif left.type() != right.type():
        return Error(f"discrepancia de tipos: {left.type()} {operator} {right.type()}")
    return Error(f"operador desconocido: {left.type()} {operator} {right.type()}")

def eval_string_infix_expression(operator, left, right):
    if operator != "+":
        return Error(f"operador desconocido: {left.type()} {operator} {right.type()}")
    return StringObj(left.value + right.value)

def eval_integer_infix_expression(operator, left, right):
    l_val = left.value
    r_val = right.value
    if operator == "+": return Integer(l_val + r_val)
    elif operator == "-": return Integer(l_val - r_val)
    elif operator == "*": return Integer(l_val * r_val)
    elif operator == "/": return Integer(l_val // r_val)
    elif operator == "**": return Integer(l_val ** r_val)
    elif operator == "<": return native_bool_to_bool_object(l_val < r_val)
    elif operator == ">": return native_bool_to_bool_object(l_val > r_val)
    elif operator == "<=": return native_bool_to_bool_object(l_val <= r_val)
    elif operator == ">=": return native_bool_to_bool_object(l_val >= r_val)
    elif operator == "==": return native_bool_to_bool_object(l_val == r_val)
    elif operator == "!=": return native_bool_to_bool_object(l_val != r_val)
    return Error(f"operador desconocido: {left.type()} {operator} {right.type()}")

def is_truthy(obj):
    if obj == NULL_OBJ or obj == FALSE_OBJ: return False
    return True

def eval_if_expression(ie, env):
    condition = evaluate(ie.condition, env)
    if is_error(condition): return condition
    if is_truthy(condition):
        return evaluate(ie.consequence, env)
    for elif_cond_node, elif_cons_node in ie.elifs:
        elif_cond = evaluate(elif_cond_node, env)
        if is_error(elif_cond): return elif_cond
        if is_truthy(elif_cond):
            return evaluate(elif_cons_node, env)
    if ie.alternative is not None:
        return evaluate(ie.alternative, env)
    return NULL_OBJ

def eval_while_expression(we, env):
    result = NULL_OBJ
    while True:
        condition = evaluate(we.condition, env)
        if is_error(condition): return condition
        if not is_truthy(condition):
            break
        result = evaluate(we.body, env)
        if is_error(result): return result
        if result is not None and result.type() == ObjType.RETURN_VALUE:
            return result
        if result is not None and result.type() == ObjType.BREAK_VALUE:
            break
    return NULL_OBJ

def eval_for_expression(fe, env):
    new_env = Environment(env)
    if fe.init is not None:
        init_res = evaluate(fe.init, new_env)
        if is_error(init_res): return init_res
    result = NULL_OBJ
    while True:
        if fe.condition is not None:
            condition = evaluate(fe.condition, new_env)
            if is_error(condition): return condition
            if not is_truthy(condition):
                break
        result = evaluate(fe.body, new_env)
        if is_error(result): return result
        if result is not None and result.type() == ObjType.RETURN_VALUE:
            return result
        if result is not None and result.type() == ObjType.BREAK_VALUE:
            break
        if fe.update is not None:
            update_res = evaluate(fe.update, new_env)
            if is_error(update_res): return update_res
    return NULL_OBJ

def eval_identifier(node, env):
    val = env.get(node.value)
    if val is not None: return val
    builtin = BUILTINS.get(node.value)
    if builtin is not None: return builtin
    return Error(f"identificador no encontrado: {node.value}")

def eval_expressions(exps, env):
    result = []
    for e in exps:
        evaluated = evaluate(e, env)
        if is_error(evaluated): return [evaluated]
        result.append(evaluated)
    return result

def apply_function(fn, args):
    if isinstance(fn, FunctionObj):
        extended_env = extend_function_env(fn, args)
        evaluated = evaluate(fn.body, extended_env)
        return unwrap_return_value(evaluated)
    elif isinstance(fn, Builtin):
        return fn.fn(*args)
    return Error(f"no es una función: {fn.type()}")

def extend_function_env(fn, args):
    env = Environment(fn.env)
    for i, param in enumerate(fn.parameters):
        if i < len(args):
            env.set(param.value, args[i])
    return env

def unwrap_return_value(obj):
    if isinstance(obj, ReturnValue): return obj.value
    return obj

def eval_index_expression(left, index):
    if left.type() == ObjType.ARRAY and index.type() == ObjType.INTEGER:
        idx = index.value
        max_idx = len(left.elements) - 1
        if idx < 0 or idx > max_idx: return NULL_OBJ
        return left.elements[idx]
    return Error(f"operador de índice no soportado para: {left.type()}")
