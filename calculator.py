#!/usr/bin/env python3
"""
コンソール電卓 (Console Calculator)
基本的な四則演算をサポートする対話型電卓
"""


def calculate(expression):
    """
    数式を評価して結果を返す
    
    Args:
        expression (str): 計算式（例: "2 + 3", "10 / 2"）
    
    Returns:
        float: 計算結果
    
    Raises:
        ValueError: 無効な式の場合
        ZeroDivisionError: ゼロ除算の場合
    """
    try:
        # eval()を安全に使用するため、許可された文字のみチェック
        allowed_chars = set('0123456789+-*/(). ')
        if not all(c in allowed_chars for c in expression):
            raise ValueError("無効な文字が含まれています")
        
        # 式を評価
        result = eval(expression)
        return result
    except ZeroDivisionError:
        raise ZeroDivisionError("ゼロで割ることはできません")
    except (SyntaxError, NameError):
        raise ValueError("無効な式です")


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
        except Exception as e:
            print(f"予期しないエラー: {e}")
            print()


if __name__ == "__main__":
    main()
