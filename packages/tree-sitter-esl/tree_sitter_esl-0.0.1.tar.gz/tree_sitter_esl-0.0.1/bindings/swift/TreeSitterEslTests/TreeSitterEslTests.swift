import XCTest
import SwiftTreeSitter
import TreeSitterEsl

final class TreeSitterEslTests: XCTestCase {
    func testCanLoadGrammar() throws {
        let parser = Parser()
        let language = Language(language: tree_sitter_esl())
        XCTAssertNoThrow(try parser.setLanguage(language),
                         "Error loading Esl grammar")
    }
}
