#include <SFML/Graphics.hpp> //graphic
#include <SFML/Audio.hpp> //music
#include <stdbool.h> //bool
#include <iostream> //cout
#include <cstdlib> //random
#include <math.h> //ceil()
#include <string>
using namespace std;


sf::RenderWindow window(sf::VideoMode(313, 245), "Scarebot");
int jspeeed = -16;
float speeed = 4.5;


class Sol
{
	private:
		int x;
		int y;
		int type;
		sf::Texture t_sol1;
		sf::Sprite s_sol1;
		sf::Texture t_sol2;
		sf::Sprite s_sol2;
		sf::Texture t_sol3;
		sf::Sprite s_sol3;
	public:
		Sol()
		{
			x = 0;
			y = 203;
			type = std::rand()/((RAND_MAX + 1u)/3);
			t_sol1.loadFromFile("images/sol 1.png");
			s_sol1.setTexture(t_sol1);

			t_sol2.loadFromFile("images/sol 2.png");
			s_sol2.setTexture(t_sol2);
			
			t_sol3.loadFromFile("images/sol 3.png");
			s_sol3.setTexture(t_sol3);
		}

		void setX(int xx) {x = xx;}
		int getX() {return x;}
		void update()
		{
			x = x-(int)speeed;
			if(x<=-33)
			{
				x = 330 + (33+x);
				type = std::rand()/((RAND_MAX + 1u)/3); //random 0 1 ou 2
			}
			if(type == 0){s_sol1.setPosition(x, y); window.draw(s_sol1);}
			else if(type == 1){s_sol2.setPosition(x, y); window.draw(s_sol2);}
			else if (type==2){s_sol3.setPosition(x, y); window.draw(s_sol3);}
		
		}
};

class Obstacle
{
	private:
		sf::Texture t_large;
		sf::Sprite s_large;
		sf::Texture t_small;
		sf::Sprite s_small;
		sf::Texture t_ghost;
		sf::Sprite s_ghost;
	public:
		Obstacle()
		{
			t_large.loadFromFile("images/large object.png");
			s_large.setTexture(t_large);
			//s_sol1.setPosition(0, 203);

			t_small.loadFromFile("images/small object.png");
			s_small.setTexture(t_small);
			//s_sol2.setPosition(0, 203);
			
			t_ghost.loadFromFile("images/fantome.png");
			s_ghost.setTexture(t_ghost);
			//s_sol3.setPosition(0,203);
		}
};

class Nuage
{
	private:
		sf::Texture t_cloud1;
		sf::Sprite s_cloud1;
		sf::Texture t_cloud2;
		sf::Sprite s_cloud2;
		sf::Texture t_cloud3;
		sf::Sprite s_cloud3;
	public:
		Nuage()
		{
			t_cloud1.loadFromFile("images/cloud1.png");
			s_cloud1.setTexture(t_cloud1);
			//s_sol1.setPosition(0, 203);

			t_cloud2.loadFromFile("images/cloud2.png");
			s_cloud2.setTexture(t_cloud2);
			//s_sol2.setPosition(0, 203);
			
			t_cloud3.loadFromFile("images/cloud3.png");
			s_cloud3.setTexture(t_cloud3);
			//s_sol3.setPosition(0,203);
		}
};

class Blob
{
	private:
		int state;
		float speed;
		int jspeed;
		int gravity;
		bool stopjump;
		bool jump;
		bool fall;
		sf::Texture t_blob;
		sf::Sprite s_blob;
		sf::Texture t_blob_crouch;
		sf::Sprite s_blob_crouch;
		sf::Texture t_blob_dead;
		sf::Sprite s_blob_dead;
		int x, y;
	public:
		Blob()
		{
			speed = speeed;
			jspeed = jspeeed;
			stopjump = false;
			jump = false;
			fall = false;
			gravity = 1;
			x = 10;
			y = 180;
			state = 0; //0 : vivant, 1 : crouch, 2 : dead
			t_blob.loadFromFile("images/blob_base.png");
			s_blob.setTexture(t_blob);
			//s_blob.setPosition(x, y);

			t_blob_crouch.loadFromFile("images/blob crouch.png");
			s_blob_crouch.setTexture(t_blob_crouch);

			t_blob_dead.loadFromFile("images/blob dead.png");
			s_blob_dead.setTexture(t_blob_dead);
		}
		void update()
		{
			
			if(state == 0 || (fall && state ==1)) //vivant	
			{
				if (jump)
				{
					y = y + jspeed;
					if(stopjump and jspeed < 0)
					{
						jspeed= int(jspeeed/4);
						stopjump = false;
					}

					if (fall) {jspeed=jspeed + 3*gravity;}
					else {jspeed=jspeed+gravity;}

					if(y>=180)
					{
					    y=180;
					    jspeed= jspeeed;
					    jump = false;
					    stopjump = false;
					    fall = false;
					}
				}
			}
			if(state == 1){s_blob_crouch.setPosition(x, y+9); window.draw(s_blob_crouch);}
			else if(state == 2){s_blob_dead.setPosition(x, y); window.draw(s_blob_dead);}
			else if (state==0){s_blob.setPosition(x, y); window.draw(s_blob);}
		}

		void setX(int coordonee_x){x = coordonee_x;}
		void setY(int coordonee_y){y = coordonee_y;}
		void setState(int stateee){state = stateee;}
		int getState() {return state;}
		void setJump(bool a) {jump = a;}
		void setStopJump(bool b) {stopjump = b;}
		void setFall(bool c) {fall = c;}
		bool getJump() {return jump;}
		bool getStopJump() {return stopjump;}
		bool getFall() {return fall;}
};

class Menu
{
	private:
		int NOMBRE_DE_CHOIX_MENU;
		int choix_menu;
		sf::Texture t_background;
		sf::Sprite s_background;
		sf::Texture t_menu;
		sf::Sprite s_menu;
		sf::Texture t_curseur;
		sf::Sprite s_curseur1; // pas les mêmes coordonnées mais même image
		sf::Sprite s_curseur2;

	public:
		Menu()
		{
			NOMBRE_DE_CHOIX_MENU = 2;
			choix_menu = 0;
			t_background.loadFromFile("images/fond_vert.png");
			s_background.setTexture(t_background);
			s_background.setPosition(0, 0);

			t_menu.loadFromFile("images/menu.png");
			s_menu.setTexture(t_menu);
			s_menu.setPosition(0, 0);
			
			t_curseur.loadFromFile("images/curseur_selection_menu_gameboy.png");
			s_curseur1.setTexture(t_curseur);
			s_curseur1.setPosition(65,102);

			s_curseur2.setTexture(t_curseur);
			s_curseur2.setPosition(65,163);

		}
		void up()
		{
			choix_menu=(choix_menu+1)%NOMBRE_DE_CHOIX_MENU;
		}
		void down()
		{
			choix_menu=(choix_menu-1)%NOMBRE_DE_CHOIX_MENU;
		}
		int get_choix_menu()
		{
			return choix_menu;
		}
		void set_choix_menu(int choix)
		{
			choix_menu = choix;
		}
		void afficher_menu()
		{
			if(choix_menu == 0)
			{
				window.clear();
				window.draw(s_background);
				window.draw(s_menu);
				window.draw(s_curseur1);
				window.display();
			}
			else
			{	
				window.clear();
				window.draw(s_background);
				window.draw(s_menu);
				window.draw(s_curseur2);
				window.display();
			}
		}
};

int main()
{
	string s_score;
	sf::Font font;
	font.loadFromFile("images/pixelmix_bold.ttf");
	sf::Text text;
	text.setFont(font); 
	text.setPosition(200,10);
	sf::Color color(48, 98, 48);
	sf::Texture t_background;
	t_background.loadFromFile("images/fond_vert.png");
	sf::Sprite s_background;
	s_background.setTexture(t_background);
	s_background.setPosition(0, 0);
	window.setVerticalSyncEnabled(false);
	window.setFramerateLimit(30);
	window.setKeyRepeatEnabled(false);

	int score = 0;
	bool stopjump = false;
	bool jump = false;
	int state = 0; //Etat : 0 = menu. 1 = jeu

	sf::Music theme;
	theme.openFromFile("Musiques/8bit.wav");
	theme.play();
	theme.setLoop(true);

	sf::SoundBuffer buffer_select;
	buffer_select.loadFromFile("Musiques/sfxMenuScarebotSelect.wav");
	sf::Sound sound_select;
	sound_select.setBuffer(buffer_select);

	sf::SoundBuffer buffer_validate;
	buffer_validate.loadFromFile("Musiques/sfxMenuScarebotValidate.wav");
	sf::Sound sound_validate;
	sound_validate.setBuffer(buffer_validate);
	
	sf::SoundBuffer buffer_gameover;
	buffer_gameover.loadFromFile("Musiques/sfxScarebotGameOver.wav");
	sf::Sound sound_gameover;
	sound_gameover.setBuffer(buffer_gameover);

	sf::SoundBuffer buffer_jump;
	buffer_jump.loadFromFile("Musiques/sfxBlobRunn3rJump.wav");
	sf::Sound sound_jump;
	sound_jump.setBuffer(buffer_jump);
	

	Menu m;
	Blob b;
	int NB_SOL = 11;
	Sol sol[NB_SOL];
	for (int i = 1; i < NB_SOL; i++ )
	{
		sol[i].setX((sol[i-1].getX())+33);
	} //on écarte chaque sol de 33px
	while (window.isOpen())
	{
		sf::Event event;
// //////////////////////////////////MENU // /////////////////////// /////////////////////
		if(state == 0)
		{
			m.afficher_menu();
			while (window.pollEvent(event))
			{
			    // check the type of the event...
				switch (event.type)
				{
				// window closed
				case sf::Event::Closed:
					window.close();
					break;

				// key pressed
				case sf::Event::KeyPressed:
					if (sf::Keyboard::isKeyPressed(sf::Keyboard::Up))
						{
							sound_select.play();
							m.up();	
						}
					else if (sf::Keyboard::isKeyPressed(sf::Keyboard::Down))
						{
							sound_select.play();
							m.down();

						}
					else if (sf::Keyboard::isKeyPressed(sf::Keyboard::Enter))
						{
							sound_validate.play();
						    //Lancer le jeu ou quitter
							if(m.get_choix_menu() == 0)
							{
								state = 1;
							}
							else
							{
								window.close();
							}

						}
					else if (sf::Keyboard::isKeyPressed(sf::Keyboard::Escape))
						{
							sound_gameover.play();
							window.close();
						}
					break;

				// we don't process other types of events
				default:
					break;
			    }
			}
		}

// //////////////////////////////////JEU en lui même // /////////////////////// /////////////////////
		else
		{
			speeed = speeed + 0.0025;
			score= score + ceil(speeed/15);
			while (window.pollEvent(event))
			{
			    // check the type of the event...
				switch (event.type)
				{
				// window closed
				case sf::Event::Closed:
					window.close();
					break;

				// key pressed
				case sf::Event::KeyPressed:
					if ((sf::Keyboard::isKeyPressed(sf::Keyboard::Down)) && b.getJump() == false && b.getState() == 0)
						{
							b.setState(1);
						}
					else if ((sf::Keyboard::isKeyPressed(sf::Keyboard::Space)) && b.getJump() == false && b.getState() == 0)
						{
							b.setJump(true);
							sound_jump.play();
						}

					else if ((sf::Keyboard::isKeyPressed(sf::Keyboard::Down)) && b.getJump() == true && b.getState() == 0)
						{
							b.setFall(true);
							b.setState(1);
						}
					else if (sf::Keyboard::isKeyPressed(sf::Keyboard::Escape))
						{
							sound_gameover.play();
							window.close();
						}
					break;

				case sf::Event::KeyReleased:

					if ((event.key.code == sf::Keyboard::Down)&& b.getState() == 1)
						{
							b.setState(0);
						}
					else if ((event.key.code == sf::Keyboard::Space)&& b.getState() == 0 && b.getJump() == true)
						{
							b.setStopJump(true);
						}
					break;
				// we don't process other types of events
				default:
					break;
			    	}
			}
			s_score = "Score: " + std::to_string(score);
			window.clear();
			window.draw(s_background);
			for (int i = 0; i < NB_SOL; i++ ){sol[i].update();}
			b.update();
			// choix de la chaîne de caractères à afficher
			text.setString(s_score);
			text.setCharacterSize(12);
			text.setFillColor(color);
			window.draw(text);
			window.display();
		}

	}

	return 0;
}