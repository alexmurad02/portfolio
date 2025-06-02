#include "Tile.h"

Tile::Tile() {
	_isMine = false;
	_isFlagged = false;
	_isRevealed = false;
}

bool Tile::isMine() {
	return _isMine;
}

bool Tile::isFlagged() {
	return _isFlagged;
}

bool Tile::isRevealed() {
	return _isRevealed;
}

void Tile::reveal() {
	_isRevealed = true;
}

int Tile::getMineCount() {
	int count = 0;
	for (int i = 0; i < _adjacent.size(); i++) {
		if (_adjacent.at(i)->isMine()) {
				count++;
		}
	}
	return count;
}

void Tile::reset() {
	_isFlagged = false;
	_isMine = false;
	_isRevealed = false;
}

void Tile::mine(bool b) {
	_isMine = b;
}

bool Tile::wasClicked() {
	if (!_isFlagged && !_isRevealed) {
		_isRevealed = true;
		if (_isMine)
			return true;
		else {
			if (getMineCount() == 0) {
				for (int i = 0; i < _adjacent.size(); i++) {
					if (!_adjacent.at(i)->isRevealed() && !_adjacent.at(i)->isFlagged()) {
						_adjacent.at(i)->wasClicked();
					}
				}
			}
			return false;
		}
	}
	return false;
}

int Tile::wasRightClicked(int numFlags) {
	if (!_isRevealed) {
		_isFlagged = !_isFlagged;
		if (_isFlagged)
			return numFlags - 1;
		return numFlags + 1;
	}
	return numFlags;
}