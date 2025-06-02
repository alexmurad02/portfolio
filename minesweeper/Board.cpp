#include "Board.h"

std::mt19937 random_mt;

int Random(int min, int max)
{
	std::uniform_int_distribution<int> dist(min, max);
	return dist(random_mt);
}

Board::Board(int cols, int rows, int numMines) {
	_cols = cols;
	_rows = rows;
	_numMines = numMines;
	_numFlags = numMines;
	tiles = new Tile**[rows];
	for (int i = 0; i < rows; i++) {
		tiles[i] = new Tile*[cols];
		for (int j = 0; j < cols; j++) {
			tiles[i][j] = new Tile();
		}
	}
	setBoard(numMines);
	for (int i = 0; i < _rows; i++) {
		for (int j = 0; j < _cols; j++) {
			tiles[i][j]->_sprite.setPosition(j * 32.0f, i * 32.0f);
			for (int u = -1; u <= 1; u++) {
				for (int v = -1; v <= 1; v++) {
					if (!(v == 0 && u == 0)) {
						if ((0 <= u + i && u + i < _rows) && (0 <= v + j && v + j < _cols)) {
							tiles[i][j]->_adjacent.push_back(tiles[u + i][v + j]);
						} 
					}
				}
			}
		}
	}
}

void Board::setBoard(int numMines) {
	_numFlags = numMines;
	_numMines = numMines;
	for (int i = 0; i < _rows; i++) {
		for (int j = 0; j < _cols; j++) {
			tiles[i][j]->reset();
		}
	}
	int x;
	for (int i = 0; i < _numMines; i++) {
		x = Random(0, (_rows * _cols) - 1);
		if (!tiles[x / _cols][x % _cols]->isMine()) {
			tiles[x / _cols][x % _cols]->mine(true);
		}
		else {
			i--;
		}
	}
}

Board::~Board() {
	for (int i = 0; i < _rows; i++) {
		for (int j = 0; j < _cols; j++) {
			delete tiles[i][j];
		}
		delete[] tiles[i];
	}
	delete[] tiles;
}