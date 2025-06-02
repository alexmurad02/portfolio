#pragma once
#include "Tile.h"
#include "SFML/Graphics.hpp"
#include <random>
#include <vector>

struct Board
{
	int _numFlags;
	int _cols;
	int _rows;
	int _numMines;
	Tile*** tiles;
	Board(int, int, int);
	void setBoard(int);
	~Board();
	sf::Sprite _digit_0;
	sf::Sprite _digit_1;
	sf::Sprite _digit_2;
	sf::Sprite _digit_3;

	sf::Sprite _face;

	sf::Sprite _debug;
	sf::Sprite _test_1;
	sf::Sprite _test_2;
	sf::Sprite _test_3;
};