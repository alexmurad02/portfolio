#pragma once
#include <SFML/Graphics.hpp>
#include <vector>

class Tile
{
	bool _isMine;
	bool _isFlagged;
	bool _isRevealed;
public:
	sf::Sprite _sprite;
	std::vector<Tile*> _adjacent;

	Tile();
	bool isMine();
	bool isFlagged();
	bool isRevealed();
	void reveal();
	int getMineCount();
	void reset();
	void mine(bool);
	bool wasClicked();
	int wasRightClicked(int);
};