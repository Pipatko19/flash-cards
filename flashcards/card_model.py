
from PySide6 import QtCore as qtc
from PySide6.QtCore import Qt

IndexType = qtc.QModelIndex | qtc.QPersistentModelIndex


class FlashCardsModel(qtc.QAbstractListModel):
    QUESTION_ROLE = Qt.ItemDataRole.UserRole + 1
    ANSWER_ROLE = Qt.ItemDataRole.UserRole + 2
    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)
        self.flashcards = []
    
    @property
    def empty(self):
        return self.flashcards == []
    
    def rowCount(self, parent = None):
        return len(self.flashcards)
    
    def data(self, index: IndexType, role: int = Qt.ItemDataRole.DisplayRole) -> str | None:
        if not index.isValid():
            return None
        row = index.row()
        if role == Qt.ItemDataRole.DisplayRole or role == FlashCardsModel.QUESTION_ROLE:
            return self.flashcards[row]['question']
        if role == FlashCardsModel.ANSWER_ROLE:
            return self.flashcards[row]['question']
        
        return None
    
    def setData(self, index: IndexType, value: str, role: int = Qt.ItemDataRole.DisplayRole) -> bool:
        card = self.flashcards[index.row()]

        match role:
            case FlashCardsModel.QUESTION_ROLE:
                card['question'] = value
            case FlashCardsModel.ANSWER_ROLE:
                card['answer'] = value
            case _:
                return False
        self.dataChanged.emit(index, index)
        #print(*(card.values() for card in self.flashcards), sep='\n')
        return True

    def removeRows(self, row: int, count: int, parent = qtc.QModelIndex()):
        if row < 0 or row + count > len(self.flashcards):
            return False
        self.beginRemoveRows(qtc.QModelIndex(), row, row + count - 1)
        for _ in range(count):
            del self.flashcards[row]
        self.endRemoveRows()
        return True

    def insertRows(self, row: int, count: int, parent = qtc.QModelIndex()):
        if row != self.rowCount() or count <= 0 or parent.isValid():
            return False
        self.beginInsertRows(qtc.QModelIndex(), row, row + count - 1)
        for _ in range(count):        
            self.flashcards.append({'question': None, 'answer': None})
        self.endInsertRows()
        return True

    def overwrite_data(self, data):
        self.beginResetModel()
        self.flashcards = data
        self.endResetModel()
        self.dataChanged.emit(self.index(0), self.index(len(self.flashcards) - 1))
        