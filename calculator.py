#!/usr/bin/env python3
"""
コンソール電卓 (Console Calculator)
基本的な四則演算をサポートする対話型電卓
"""

import ast
import operator


def calculate(expression):
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
    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }
    
    def _eval_node(node):
        """ASTノードを安全に評価"""
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.BinOp):
            left = _eval_node(node.left)
            right = _eval_node(node.right)
            op = operators.get(type(node.op))
            if op is None:
                raise ValueError("サポートされていない演算子です")
            if isinstance(node.op, ast.Div) and right == 0:
                raise ZeroDivisionError("ゼロで割ることはできません")
            return op(left, right)
        elif isinstance(node, ast.UnaryOp):
            operand = _eval_node(node.operand)
            op = operators.get(type(node.op))
            if op is None:
                raise ValueError("サポートされていない演算子です")
            return op(operand)
        else:
            raise ValueError("サポートされていない式です")
    
    try:
        # 式をASTに解析
        tree = ast.parse(expression, mode='eval')
        # ASTを評価
        result = _eval_node(tree.body)
        return result
    except ZeroDivisionError:
        raise
    except (SyntaxError, ValueError):
        raise ValueError("無効な式です")
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
    print("終了するには 'q' または 'quit' を入力してください")
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
