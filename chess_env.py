class CastlingRights:
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


class GameState:
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]

        ]
        self.pieceMoveFunctions = {"p": self.pawnMoves, "R": self.rookMoves, "N": self.knightMoves, "B": self.bishopMoves, "Q": self.queenMoves, "K": self.kingMoves}
        self.isCheckmate = False
        self.isStalemate = False
        self.isCheck = False
        self.isWhiteMove = True
        self.pins = []
        self.checks = []
        self.moveLog = []
        self.enpassantCaptureCoordinates = ()
        self.enpassantCaptureCoordinatesLog = [self.enpassantCaptureCoordinates]
        self.castlingRights = CastlingRights(True, True, True, True)
        self.castlingRightsLog = [CastlingRights(self.castlingRights.wks, self.castlingRights, self.castlingRights.wqs, self.castlingRights.bqs)]
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)

        def executeMove(self, move):
            self.board[move.startRow][move.startCol] = "--"
            self.board[move.endRow][move.endCol] = move.pieceMoved
            self.moveLog.append(move)
            self.isWhiteMove = not self.isWhiteMove
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.endRow, move.endCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.endRow, move.endCol)

            if move.isPawnPromotion:
                self.board[move.endRow][move.endCol] = move.pieceMoved[0] + "Q"

            if move.isEnpassantMove:
                self.board[move.startRow][move.endCol] = "--"

            if move.pieceMoved[1] == "p" and abs(move.startRow - move.endRow) == 2:
                self.enpassantCaptureCoordinates = ((move.startRow + move.endRow) // 2, move.startCol)
            else:
                self.enpassantCaptureCoordinates = ()

            if move.isCastleMove:
                if move.endCol - move.startCol == 2:
                    self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = "--"
                else:
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]
                    self.board[move.endRow][move.endCol - 2] = "--"
            self.enpassantCaptureCoordinatesLog.append(self.enpassantCaptureCoordinates)

            self.updateCastlingRights(move)
            self.castlingRightsLog.append(CastlingRights(self.castlingRights.wks, self.castlingRights.bks, self.castlingRights.wqs,
                                                         self.castlingRights.bqs))

        def updateCastlingRights(self, move):
            if move.pieceCaptured == "wR":
                if move.endCol == 0:
                    self.castlingRights.wqs = False
                elif move.endCol == 7:
                    self.castlingRights.wks = False
            elif move.pieceCaptured == "bR":
                if move.endCol == 0:
                    self.castlingRights.bqs = False
                elif move.endCol == 7:
                    self.castlingRights.bks = False

            if move.pieceMoved == "bK":
                self.castlingRights.bqs = False
                self.castlingRights.bks = False
            elif move.pieceMoved == "wK":
                self.castlingRights.wqs = False
                self.castlingRights.wks = False
            elif move.pieceMoved == "bR":
                if move.startRow == 0:
                    if move.startCol == 0:
                        self.castlingRights.bqs = False
                    elif move.startCol == 7:
                        self.castlingRights.bks = False
            elif move.pieceMoved == "wR":
                if move.startRow == 7:
                    if move.startCol == 0:
                        self.castlingRights.wqs = False
                    elif move.startCol == 7:
                        self.castlingRights.wks = False

        def validMoves(self):
            tempCastlingRights = CastlingRights(self.castlingRights.wks, self.castlingRights.bks,
                                                self.castlingRights.wqs, self.castlingRights.bqs)

            moves = []
            self.isCheck, self.pins, self.checks = self.searchPinsandChecks()

            if self.isWhiteMove:
                kingRow = self.whiteKingLocation[0]
                kingCol = self.whiteKingLocation[1]
            else:
                kingRow = self.blackKingLocation[0]
                kingCol = self.blackKingLocation[1]
            if self.isCheck:
                if len(self.checks) == 1:
                    moves = self.getPossibleMoves()
                    check = self.checks[0]
                    checkRow = check[0]
                    checkCol = check[1]
                    pieceChecking = self.board[checkRow][checkCol]
                    validSquares = []
                    if pieceChecking[1] == "N":
                        validSquares = [(checkRow, checkCol)]
                    else:
                        for i in range(1, 8):
                            validSquare = (kingRow)








