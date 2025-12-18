#!/usr/bin/env python3
"""
コンソール電卓 (Console Calculator)
基本的な四則演算をサポートする対話型電卓
"""

import operator
import re
from collections import namedtuple
from typing import Union

# namedtuple定義
InfixOp = namedtuple('InfixOp', ['op'])
PrefixOp = namedtuple('PrefixOp', ['op'])
Paren = namedtuple('Paren', [])

Token = Union[float, InfixOp, PrefixOp]


def calculate(expression: str) -> float:
    """
    数式を評価して結果を返す（安全な方法で）
    
    Args:
        expression (str): 計算式（例: "2 + 3", "10 / 2"）
    
    Returns:
        float: 計算結果
    
    Raises:
        ValueError: 無効な式の場合
        ZeroDivisionError: ゼロ除算の場合
    """
    # 許可する演算子の定義
    infix_operators = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
    }
    prefix_operators = {
        '-': operator.neg,
    }

    def tokenize(expr: str) -> list[str]:
        """式をトークンに分割"""
        # 空白で区切った後、各部分を正規表現で分割
        parts = expr.split()
        tokens = []
        for part in parts:
            while part:
                match = re.match(r'\d+(?:\.\d+)?|[+\-*/()]', part)
                if match:
                    tokens.append(match.group())
                    part = part[match.end():]
                else:
                    raise ValueError(f"無効なトークン: {part}")
        return tokens

    def parse_expression(expr: str) -> list[Token]:
        """操車場アルゴリズムを用いて式を評価"""
        tokens = tokenize(expr)
        stack: list[Union[InfixOp, PrefixOp, Paren]] = []
        output: list[Token] = []
        after_exp: bool = False  # False: 式の前（式が必要）、True: 式の後（演算子が必要）
        
        infix_precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        prefix_precedence = {'-': 3}
        
        for token in tokens:
            if re.match(r'\d+(?:\.\d+)?', token):
                if after_exp:
                    raise ValueError("式の連続は無効です")
                output.append(float(token))
                after_exp = True
            elif token == '(':
                stack.append(Paren())
                after_exp = False
            elif token == ')':
                while stack:
                    stack_head = stack[-1]
                    if isinstance(stack_head, Paren):
                        break
                    output.append(stack_head)
                    stack.pop()
                if stack and isinstance(stack[-1], Paren):
                    stack.pop()
                else:
                    raise ValueError("括弧の不一致")
                after_exp = True
            elif token in '+-*/':
                if token == '-' and not after_exp:
                    # 前置-
                    while stack:
                        stack_head = stack[-1]
                        if not (isinstance(stack_head, PrefixOp) and
                               prefix_precedence['-'] <= prefix_precedence[stack_head.op]):
                            break
                        output.append(stack_head)
                        stack.pop()
                    stack.append(PrefixOp('-'))
                    after_exp = False
                else:
                    # 中置
                    if not after_exp:
                        raise ValueError("演算子の前に式が必要です")
                    while stack:
                        stack_head = stack[-1]
                        if not (isinstance(stack_head, InfixOp) and
                               infix_precedence[token] <= infix_precedence[stack_head.op]):
                            break
                        output.append(stack_head)
                        stack.pop()
                    stack.append(InfixOp(token))
                    after_exp = False
            else:
                raise AssertionError(f"予期しないトークン: {token}")
        
        if not after_exp:
            raise ValueError("式が不完全です")
        
        while stack:
            stack_head = stack[-1]
            if isinstance(stack_head, Paren):
                raise ValueError("括弧の不一致")
            output.append(stack_head)
            stack.pop()
        
        return output

    def evaluate_rpn(rpn: list[Token]) -> float:
        """逆ポーランド記法で評価"""
        stack: list[float] = []
        for token in rpn:
            if isinstance(token, float):
                stack.append(token)
            elif isinstance(token, PrefixOp):
                operand = stack.pop()
                stack.append(prefix_operators[token.op](operand))
            elif isinstance(token, InfixOp):
                right = stack.pop()
                left = stack.pop()
                op = infix_operators[token.op]
                if token.op == '/' and right == 0:
                    raise ZeroDivisionError("ゼロで割ることはできません")
                stack.append(op(left, right))
            else:
                raise AssertionError(f"予期しないトークン: {token}")
        return stack[0]

    try:
        # 式をパース
        rpn = parse_expression(expression)
        # RPNを評価
        result = evaluate_rpn(rpn)
        return result
    except (ValueError, ZeroDivisionError):
        raise
    except Exception as e:
        raise ValueError(f"式の評価中にエラーが発生しました: {e}")


def main():
    """
    メインの電卓ループ
    """
    print("=" * 50)
    print("コンソール電卓")
    print("=" * 50)
    print("使い方: 計算式を入力してください（例: 2 + 3）")
    print("対応演算: + (加算), - (減算), * (乗算), / (除算)")
    print("終了するには 'q', 'quit', または 'exit' を入力してください")
    print("=" * 50)
    print()
    
    while True:
        try:
            # ユーザー入力を取得
            user_input = input(">>> ").strip()
            
            # 終了コマンドのチェック
            if user_input.lower() in ['q', 'quit', 'exit']:
                print("電卓を終了します。")
                break
            
            # 空入力のチェック
            if not user_input:
                continue
            
            # 計算実行
            result = calculate(user_input)
            print(f"結果: {result}")
            print()
            
        except ValueError as e:
            print(f"エラー: {e}")
            print()
        except ZeroDivisionError as e:
            print(f"エラー: {e}")
            print()
        except KeyboardInterrupt:
            print("\n電卓を終了します。")
            break


if __name__ == "__main__":
    main()
