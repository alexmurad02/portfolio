#include <SFML/Graphics.hpp>
#include <map>
#include <string>
#include <fstream>
#include "Tile.h"
#include "Board.h"
#include <vector>

std::string toStr(int n) {
	if (n == 1)
		return "one";
	if (n == 2)
		return "two";
	if (n == 3)
		return "three";
	if (n == 4)
		return "four";
	if (n == 5)
		return "five";
	if (n == 6)
		return "six";
	if (n == 7)
		return "seven";
	if (n == 8)
		return "eight";
}

void drawTile(sf::RenderWindow& w, Tile& tile, std::map<std::string, sf::Texture>& textureMap, bool victory, bool defeat, bool debug) {
	if (defeat) {
		if (tile.isMine()) {
			tile._sprite.setTexture(textureMap["tile r"]);
			w.draw(tile._sprite);
			if (tile.isFlagged()) {
				tile._sprite.setTexture(textureMap["flag"]);
				w.draw(tile._sprite);
			}
			tile._sprite.setTexture(textureMap["mine"]);
			w.draw(tile._sprite);

		}
		else if (tile.isRevealed()) {
			tile._sprite.setTexture(textureMap["tile r"]);
			w.draw(tile._sprite);
			if (!(tile.getMineCount() == 0)) {
				tile._sprite.setTexture(textureMap[toStr(tile.getMineCount())]);
				w.draw(tile._sprite);
			}
		}
		else {
			tile._sprite.setTexture(textureMap["tile h"]);
			w.draw(tile._sprite);
			if (tile.isFlagged()) {
				tile._sprite.setTexture(textureMap["flag"]);
				w.draw(tile._sprite);
			}
		}
	}
	else if(victory) {
		if (tile.isMine()) {
			tile._sprite.setTexture(textureMap["tile h"]);
			w.draw(tile._sprite);
			tile._sprite.setTexture(textureMap["flag"]);
			w.draw(tile._sprite);
		}
		else {
			tile._sprite.setTexture(textureMap["tile r"]);
			w.draw(tile._sprite);
			if (!(tile.getMineCount() == 0)) {
				tile._sprite.setTexture(textureMap[toStr(tile.getMineCount())]);
				w.draw(tile._sprite);
			}
		}
	}
	else {
		if (tile.isRevealed()) {
			tile._sprite.setTexture(textureMap["tile r"]);
			w.draw(tile._sprite);
			if (!(tile.getMineCount() == 0)) {
				tile._sprite.setTexture(textureMap[toStr(tile.getMineCount())]);
				w.draw(tile._sprite);
			}
		}
		else {
			tile._sprite.setTexture(textureMap["tile h"]);
			w.draw(tile._sprite);
			if (tile.isFlagged()) {
				tile._sprite.setTexture(textureMap["flag"]);
				w.draw(tile._sprite);
			}
		}
		if (debug) {
			if (tile.isMine()) {
				tile._sprite.setTexture(textureMap["mine"]);
				w.draw(tile._sprite);
			}
		}
	}
}

int getDigit(Board& b, int d) {
	if (d == 1) {
		return abs(b._numFlags / 100) * 21;
	}
	else if (d == 2) {
		return abs((b._numFlags % 100) / 10) * 21;
	}
	else if (d == 3) {
		return abs(b._numFlags % 10) * 21;
	}
}

void drawUI(sf::RenderWindow& w, Board& board, std::map<std::string, sf::Texture>& textureMap, bool victory, bool defeat) {
	if (defeat) {
		board._face.setTexture(textureMap["face l"]);
	}
	else if (victory) {
		board._face.setTexture(textureMap["face w"]);
	}
	else {
		board._face.setTexture(textureMap["face h"]);
	}
	board._digit_0.setTextureRect(sf::IntRect(210, 0, 21, 32));
	board._digit_1.setTextureRect(sf::IntRect(getDigit(board, 1), 0, 21, 32));
	board._digit_2.setTextureRect(sf::IntRect(getDigit(board, 2), 0, 21, 32));
	board._digit_3.setTextureRect(sf::IntRect(getDigit(board, 3), 0, 21, 32));
	
	if (board._numFlags < 0) {
		w.draw(board._digit_0);
	}

	w.draw(board._digit_1);
	w.draw(board._digit_2);
	w.draw(board._digit_3);

	w.draw(board._face);
	w.draw(board._debug);
	w.draw(board._test_1);
	w.draw(board._test_2);
	w.draw(board._test_3);
}

int main()
{
	std::ifstream file("boards/config.cfg");
	std::string temp;
	int numCols;
	std::getline(file, temp);
	numCols = std::stoi(temp);
	int numRows;
	std::getline(file, temp);
	numRows = std::stoi(temp);
	int numMines;
	std::getline(file, temp);
	numMines = std::stoi(temp);
	
	int mineCount[3] = { 0, 0, 0 };
	std::vector<bool> testboard1;
	file = std::ifstream("boards/testboard1.brd");
	for (int i = 0; i < numRows; i++) {
		std::getline(file, temp);
		for (int j = 0; j < temp.size(); j++) {
			if (temp.at(j) == '0') {
				testboard1.push_back(false);
			}
			else {
				testboard1.push_back(true);
				mineCount[0]++;
			}
		}
	}

	std::vector<bool> testboard2;
	file = std::ifstream("boards/testboard2.brd");
	for (int i = 0; i < numRows; i++) {
		std::getline(file, temp);
		for (int j = 0; j < temp.size(); j++) {
			if (temp.at(j) == '0') {
				testboard2.push_back(false);
			}
			else {
				testboard2.push_back(true);
				mineCount[1]++;
			}
		}
	}

	std::vector<bool> testboard3;
	file = std::ifstream("boards/testboard3.brd");
	for (int i = 0; i < numRows; i++) {
		std::getline(file, temp);
		for (int j = 0; j < temp.size(); j++) {
			if (temp.at(j) == '0') {
				testboard3.push_back(false);
			}
			else {
				testboard3.push_back(true);
				mineCount[2]++;
			}
		}
	}

	sf::RenderWindow window(sf::VideoMode(numCols * 32, numRows * 32 + 100), "Minesweeper", sf::Style::Close | sf::Style::Titlebar);

	std::map<std::string,sf::Texture> textures;

	textures.emplace("mine", sf::Texture());
	textures.emplace("tile h", sf::Texture());
	textures.emplace("tile r", sf::Texture());
	textures.emplace("one", sf::Texture());
	textures.emplace("two", sf::Texture());
	textures.emplace("three", sf::Texture());
	textures.emplace("four", sf::Texture());
	textures.emplace("five", sf::Texture());
	textures.emplace("six", sf::Texture());
	textures.emplace("seven", sf::Texture());
	textures.emplace("eight", sf::Texture());
	textures.emplace("flag", sf::Texture());
	textures.emplace("face h", sf::Texture());
	textures.emplace("face w", sf::Texture());
	textures.emplace("face l", sf::Texture());
	textures.emplace("digits", sf::Texture());
	textures.emplace("debug", sf::Texture());
	textures.emplace("test 1", sf::Texture());
	textures.emplace("test 2", sf::Texture());
	textures.emplace("test 3", sf::Texture());
	textures["mine"].loadFromFile("images/mine.png");
	textures["tile h"].loadFromFile("images/tile_hidden.png");
	textures["tile r"].loadFromFile("images/tile_revealed.png");
	textures["one"].loadFromFile("images/number_1.png");
	textures["two"].loadFromFile("images/number_2.png");
	textures["three"].loadFromFile("images/number_3.png");
	textures["four"].loadFromFile("images/number_4.png");
	textures["five"].loadFromFile("images/number_5.png");
	textures["six"].loadFromFile("images/number_6.png");
	textures["seven"].loadFromFile("images/number_7.png");
	textures["eight"].loadFromFile("images/number_8.png");
	textures["flag"].loadFromFile("images/flag.png");
	textures["face h"].loadFromFile("images/face_happy.png");
	textures["face w"].loadFromFile("images/face_win.png");
	textures["face l"].loadFromFile("images/face_lose.png");
	textures["digits"].loadFromFile("images/digits.png");
	textures["debug"].loadFromFile("images/debug.png");
	textures["test 1"].loadFromFile("images/test_1.png");
	textures["test 2"].loadFromFile("images/test_2.png");
	textures["test 3"].loadFromFile("images/test_3.png");

	Board board(numCols, numRows, numMines);
	board._debug.setTexture(textures["debug"]);
	board._test_1.setTexture(textures["test 1"]);
	board._test_2.setTexture(textures["test 2"]);
	board._test_3.setTexture(textures["test 3"]);
	board._digit_0.setTexture(textures["digits"]);
	board._digit_1.setTexture(textures["digits"]);
	board._digit_2.setTexture(textures["digits"]);
	board._digit_3.setTexture(textures["digits"]);
	
	board._face.setPosition(32 * (numCols / 2.0f) - 32, 32 * numRows);
	board._debug.setPosition(32 * (numCols / 2.0f) + 96, 32 * numRows);
	board._test_1.setPosition(32 * (numCols / 2.0f) + 160, 32 * numRows);
	board._test_2.setPosition(32 * (numCols / 2.0f) + 224, 32 * numRows);
	board._test_3.setPosition(32 * (numCols / 2.0f) + 288, 32 * numRows);
	board._digit_0.setPosition(0, 32 * numRows);
	board._digit_1.setPosition(21, 32 * numRows);
	board._digit_2.setPosition(42, 32 * numRows);
	board._digit_3.setPosition(63, 32 * numRows);

	bool victory = false;
	bool defeat = false;
	bool debug = false;

	while (window.isOpen())
	{
		sf::Event event;
		while (window.pollEvent(event))
		{
			if (event.type == sf::Event::Closed)
			{
				window.close();
			}
			else if (event.type == sf::Event::MouseButtonPressed) {
				sf::Vector2i mousePosition;
				if (sf::Mouse::isButtonPressed(sf::Mouse::Left)) {
					mousePosition = sf::Mouse::getPosition(window);
					if ((board._face.getPosition().x <= mousePosition.x && mousePosition.x < board._face.getPosition().x + 64) &&
						(board._face.getPosition().y <= mousePosition.y && mousePosition.y < board._face.getPosition().y + 64)) {
						victory = false;
						defeat = false;
						board.setBoard(numMines);
					}
					else if ((board._test_1.getPosition().x <= mousePosition.x && mousePosition.x < board._test_1.getPosition().x + 64) &&
						(board._test_1.getPosition().y <= mousePosition.y && mousePosition.y < board._test_1.getPosition().y + 64)) {
						victory = false;
						defeat = false;
						board.setBoard(mineCount[0]);
						for (int i = 0; i < numRows; i++) {
							for (int j = 0; j < numCols; j++) {
								if (testboard1.at((i * numCols) + j)) {
									board.tiles[i][j]->mine(true);
								}
								else {
									board.tiles[i][j]->mine(false);
								}
							}
						}
					}
					else if ((board._test_2.getPosition().x <= mousePosition.x && mousePosition.x < board._test_2.getPosition().x + 64) &&
						(board._test_2.getPosition().y <= mousePosition.y && mousePosition.y < board._test_2.getPosition().y + 64)) {
						victory = false;
						defeat = false;
						board.setBoard(mineCount[1]);
						for (int i = 0; i < numRows; i++) {
							for (int j = 0; j < numCols; j++) {
								if (testboard2.at((i * numCols) + j)) {
									board.tiles[i][j]->mine(true);
								}
								else {
									board.tiles[i][j]->mine(false);
								}
							}
						}
					}
					else if ((board._test_3.getPosition().x <= mousePosition.x && mousePosition.x < board._test_3.getPosition().x + 64) &&
						(board._test_3.getPosition().y <= mousePosition.y && mousePosition.y < board._test_3.getPosition().y + 64)) {
						victory = false;
						defeat = false;
						board.setBoard(mineCount[2]);
						for (int i = 0; i < numRows; i++) {
							for (int j = 0; j < numCols; j++) {
								if (testboard3.at((i * numCols) + j)) {
									board.tiles[i][j]->mine(true);
								}
								else {
									board.tiles[i][j]->mine(false);
								}
							}
						}
					}
				}
				if (!victory && !defeat) {
					if (sf::Mouse::isButtonPressed(sf::Mouse::Left)) {
						mousePosition = sf::Mouse::getPosition(window);
						if ((0 <= mousePosition.x && mousePosition.x < board._cols * 32) &&
							(0 <= mousePosition.y && mousePosition.y < board._rows * 32)) {
							defeat = board.tiles[mousePosition.y / 32][mousePosition.x / 32]->wasClicked();
						}
						else if ((board._debug.getPosition().x <= mousePosition.x && mousePosition.x < board._debug.getPosition().x + 64) &&
							(board._debug.getPosition().y <= mousePosition.y && mousePosition.y < board._debug.getPosition().y + 64)) {
							debug = !debug;
						}
					}
					else if (sf::Mouse::isButtonPressed(sf::Mouse::Right)) {
						mousePosition = sf::Mouse::getPosition(window);
						if ((0 <= mousePosition.x && mousePosition.x < board._cols * 32) &&
							(0 <= mousePosition.y && mousePosition.y < board._rows * 32)) {
							board._numFlags = board.tiles[mousePosition.y / 32][mousePosition.x / 32]->wasRightClicked(board._numFlags);
						}
					}
				}
			}
		}

		int count = 0;
		for (int i = 0; i < board._rows; i++) {
			for (int j = 0; j < board._cols; j++) {
				if (board.tiles[i][j]->isRevealed()) {
					count++;
				}
			}
		}
		if (board._cols * board._rows == count + board._numMines) {
			victory = true;
			board._numFlags = 0;
		}

		window.clear();
		
		for (int i = 0; i < board._rows; i++) {
			for (int j = 0; j < board._cols; j++) {
				drawTile(window, *board.tiles[i][j], textures, victory, defeat, debug);
			}
		}

		drawUI(window, board, textures, victory, defeat);

		window.display();
	}

	return 0;
}