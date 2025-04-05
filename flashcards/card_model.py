from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg
from PySide6.QtCore import Qt

class FlashCardsModel(qtc.QAbstractListModel):
    QUESTION_ROLE = Qt.UserRole + 1
    ANSWER_ROLE = Qt.UserRole + 2
    def __init__(self, flashcards: list = None, *args,**kwargs):
        super().__init__(*args, **kwargs)
        self.flashcards = flashcards or []
    
    def rowCount(self, parent = None):
        return len(self.flashcards)
    
    def data(self, index: qtc.QModelIndex, role: Qt.ItemDataRole) -> str:
        if not index.isValid():
            return None
        row = index.row()
        if role == qtc.Qt.DisplayRole or role == FlashCardsModel.QUESTION_ROLE:
            return self.flashcards[row]['question']
        if role == FlashCardsModel.ANSWER_ROLE:
            return self.flashcards[row]['question']
    
    def setData(self, index: qtc.QModelIndex, value: str, role: int) -> bool:
        card = self.flashcards[index.row()]

        match role:
            case FlashCardsModel.QUESTION_ROLE:
                card['question'] = value
            case FlashCardsModel.ANSWER_ROLE:
                card['answer'] = value
            case _:
                return False
        self.dataChanged.emit(index, index)
        print(*(card.values() for card in self.flashcards), sep='\n')
        return True

    def removeRow(self, row, parent = None):
        row -= 1
        if 0 <= row < len(self.flashcards):
            self.beginRemoveRows(qtc.QModelIndex(), row, row)
            del self.flashcards[row]
            self.endRemoveRows()
            return True
        return False

    def insertRow(self, row, parent = None):
        self.beginInsertRows(qtc.QModelIndex(), row, row)
        self.flashcards.append({'question': None, 'answer': None})
        self.endInsertRows()

    def overwrite_data(self, data):
        self.beginResetModel()
        self.flashcards = data
        self.endResetModel()
        self.dataChanged.emit(self.index(0), self.index(len(self.flashcards) - 1))
        