import unittest
import jack_analyzer.jack_tokenizer as jt
import pdb

class TestJackTokenizer(unittest.TestCase):
    def setUp(self):
        self.tokenizer = jt.JackTokenizer(r"C:\Users\verno\OneDrive\Documents\nand2tetris\projects\10\ArrayTest\Main.jack")

    def test_tokentype_keyword(self):
        self.tokenizer._set_current_token("class")
        self.assertEqual(self.tokenizer.token_type(), jt.JackTokenType.KEYWORD, "Failed to parse keyword")
        
    def test_tokentype_symbol(self):
        self.tokenizer._set_current_token("=")
        self.assertEqual(self.tokenizer.token_type(), jt.JackTokenType.SYMBOL, "Failed to parse equals")

    def test_tokentype_identifier(self):
        self.tokenizer._set_current_token("x")
        self.assertEqual(self.tokenizer.token_type(), jt.JackTokenType.IDENTIFIER, "Failed to parse identifier")

    def test_tokentype_string_const(self):
        self.tokenizer._set_current_token('"nand2tetris"')
        self.assertEqual(self.tokenizer.token_type(), jt.JackTokenType.STRING_CONST, "Failed to parse string constant")

    def test_tokentype_int_const(self):
        self.tokenizer._set_current_token("122")
        self.assertEqual(self.tokenizer.token_type(), jt.JackTokenType.INT_CONST, "Failed to parse integer constant")

    def test_tokentype_invalid(self):
        self.tokenizer._set_current_token("2abc222")
        try:
            self.tokenizer.token_type()
        except jt.InvalidToken:
            pass
        except Exception:
            self.fail("Unexpected exception raise")
        else:
            self.fail("InvalidToken exception not raised")

    def test_valid_identifier_correct1(self):
        self.assertTrue(self.tokenizer._valid_identifier("abc2"), "Failed to validate correct identifier")
        
    def test_valid_identifier_correct2(self):
        self.assertTrue(self.tokenizer._valid_identifier("ab_c2"), "Failed to validate identifier with underscore")
        
    def test_valid_identifier_wrong1(self):
        self.assertFalse(self.tokenizer._valid_identifier("2abc2"), "Said identifier starting with number was valid")

    def test_valid_identifier_wrong2(self):
        self.assertFalse(self.tokenizer._valid_identifier("abc\\3"), "Said identifier with backslash was valid")

    def tearDown(self):
        self.tokenizer.close()

if __name__ == "__main__":
    unittest.main()
