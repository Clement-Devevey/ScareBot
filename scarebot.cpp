#include <SFML/Graphics.hpp> //graphic
#include <SFML/Audio.hpp> //music
#include "Collision.h"
#include <stdbool.h> //bool
#include <cstdlib> //random
#include <math.h> //ceil()
#include <string>
using namespace std;
int xwin = 313;
int ywin = 245;
sf::RenderWindow window(sf::VideoMode(xwin, ywin), "Scarebot");
int jspeeed = -16;
float speeed = 4.5;
int plus_un = 0; //variable pour régler les nuages à leur bon emplacement

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
		void Reset()
		{
			type = std::rand()/((RAND_MAX + 1u)/3);
		}
		void setX(int xx) {x = xx;}
		int getX() {return x;}
		void draw()
		{
			if(type == 0){s_sol1.setPosition(x, y); window.draw(s_sol1);}
			else if(type == 1){s_sol2.setPosition(x, y); window.draw(s_sol2);}
			else if (type==2){s_sol3.setPosition(x, y); window.draw(s_sol3);}
		}
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
		int x,y,type;
	public:
		sf::Texture t_large;
		sf::Texture t_small;
		sf::Texture t_ghost;
		sf::Sprite s_large;
		sf::Sprite s_small;
		sf::Sprite s_ghost;
		Obstacle()
		{
			t_large.loadFromFile("images/large object.png");
			s_large.setTexture(t_large);
			//s_sol1.setPosition(0, 203);

			t_small.loadFromFile("images/small object.png");
			s_small.setTexture(t_small);
			//s_sol2.setPosition(0, 203);
			
			t_ghost.loadFromFile("images/fantome gameboy.png");
			s_ghost.setTexture(t_ghost);
			//s_sol3.setPosition(0,203);
			x=330 + std::rand()/((RAND_MAX + 1u)/300);
			y=197;
		}
		void Reset()
		{
			//Faut reset la position du sprite loin sinon quand on relance le sprite est tjrs la ><
			//if(type == 0){s_small.setPosition(x-50, y);}
			//else if(type == 1){s_large.setPosition(x-50, y); }
			//else if (type==2){s_ghost.setPosition(x-50, y-63);}

			x=330 + std::rand()/((RAND_MAX + 1u)/300);
			type = type+1;
			if(type>3){type = 0;}
		}
		int getX() {return x;}
		int getY() {return y;}
		int getType() {return type;}
		void setX(int a) {x=a;}
		void setY(int b) {y=b;}
		void setType(int c) {type=c;}	
		void draw()
		{
			if(type == 0){s_small.setPosition(x, y); window.draw(s_small);}
			else if(type == 1){s_large.setPosition(x, y); window.draw(s_large);}
			else if (type==2){s_ghost.setPosition(x, y-63); window.draw(s_ghost);}
		}
		void update()
		{
			x =x-(int)speeed;
			if(x<-50)
			{
				x=330 + std::rand()/((RAND_MAX + 1u)/300);
				type = std::rand()/((RAND_MAX + 1u)/3);
			}
			if(type == 0){s_small.setPosition(x, y); window.draw(s_small);}
			else if(type == 1){s_large.setPosition(x, y); window.draw(s_large);}
			else if (type==2){s_ghost.setPosition(x, y-63); window.draw(s_ghost);}
			
			
			
		}
};

class Cloud
{
	private:
		sf::Texture t_cloud1;
		sf::Sprite s_cloud1;
		sf::Texture t_cloud2;
		sf::Sprite s_cloud2;
		sf::Texture t_cloud3;
		sf::Sprite s_cloud3;
		int x,y,type;
		int area;
	public:
		Cloud()
		{
			t_cloud1.loadFromFile("images/cloud 1.png");
			s_cloud1.setTexture(t_cloud1);

			t_cloud2.loadFromFile("images/cloud 2.png");
			s_cloud2.setTexture(t_cloud2);
			
			t_cloud3.loadFromFile("images/cloud 3.png");
			s_cloud3.setTexture(t_cloud3);
			type=std::rand()/((RAND_MAX + 1u)/3);
			area = plus_un;
			plus_un = plus_un+1;
			x=330 + std::rand()/((RAND_MAX + 1u)/300);
			if(area==0){y= 28 + std::rand()/((RAND_MAX + 1u)/40);}
			else if(area==1){y= 80 + std::rand()/((RAND_MAX + 1u)/40);}
			else if(area==2){y= 127 + std::rand()/((RAND_MAX + 1u)/40);}
			
		}

		void Reset()
		{
			if(area==0){y= 28 + std::rand()/((RAND_MAX + 1u)/47);}
			else if(area==1){y= 75 + std::rand()/((RAND_MAX + 1u)/47);}
			else if(area==2){y= 122 + std::rand()/((RAND_MAX + 1u)/48);}
			type=std::rand()/((RAND_MAX + 1u)/3);
			x=330 + std::rand()/((RAND_MAX + 1u)/200);
		}
		void draw()
		{
			if(type == 0){s_cloud1.setPosition(x, y); window.draw(s_cloud1);}
			else if(type == 1){s_cloud2.setPosition(x, y); window.draw(s_cloud2);}
			else if (type==2){s_cloud3.setPosition(x, y); window.draw(s_cloud3);}
		}
		void update()
		{
			//Vitesse de déplacement du nuage en fonction de sa coordonnée y :
			if(area==0){x=x-int(0.5*speeed);}
			else if(area==1){x=x-int(0.65*speeed);}
			else if(area==2){x=x-int(0.8*speeed);}

			//On check si le nuage est en dehors de l'écran :
			if(x<=-141)
			{
				if(area==0){y= 28 + std::rand()/((RAND_MAX + 1u)/47);}
				else if(area==1){y= 75 + std::rand()/((RAND_MAX + 1u)/47);}
				else if(area==2){y= 122 + std::rand()/((RAND_MAX + 1u)/48);}
				type=std::rand()/((RAND_MAX + 1u)/3);
				x=330 + std::rand()/((RAND_MAX + 1u)/200);
				
			}
			
			//MAJ position + affichage sur l'écran
			if(type == 0){s_cloud1.setPosition(x, y); window.draw(s_cloud1);}
			else if(type == 1){s_cloud2.setPosition(x, y); window.draw(s_cloud2);}
			else if (type==2){s_cloud3.setPosition(x, y); window.draw(s_cloud3);}
		}
		int getX() {return x;}
		int getY() {return y;}
		int getType() {return type;}
		void setX(int a) {x=a;}
		void setY(int b) {y=b;}
		void setType(int c) {type=c;}	
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
		int x, y;
	public:
		sf::Texture t_blob;
		sf::Texture t_blob_crouch;
		sf::Texture t_blob_dead;
		sf::Sprite s_blob;
		sf::Sprite s_blob_crouch;
		sf::Sprite s_blob_dead;

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
		void Reset()
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
		}
		void update()
		{
			if(state == 2){s_blob_dead.setPosition(x, y); window.draw(s_blob_dead);}
			else
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
				else if (state==0){s_blob.setPosition(x, y); window.draw(s_blob);}
			}

			
			
		}

		void setX(int coordonee_x){x = coordonee_x;}
		void setY(int coordonee_y){y = coordonee_y;}
		int getX(){return x;}
		int getY(){return y;}
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
		void Reset()
		{
			set_choix_menu(0);
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

void death(int* state, Sol sol[11], Cloud cloud[3], Obstacle* o, Blob* b, Menu* m, sf::Sound* sound_gameover, int* NB_SOL, sf::Sprite* s_background, sf::Sprite* s_gameover, sf::Text* text)
{
	*state = 0;
	jspeeed = -16;
	speeed = 4.5;
	window.clear();
	window.draw(*s_background);
	for (int i = 0; i < *NB_SOL; i++ ){sol[i].draw();}
	for (int i = 0; i < 3; i++ ){cloud[i].draw();}
	o->draw();
	b->update();
	window.draw(*text);
	window.draw(*s_gameover);
	window.display();
	m->Reset();
	sound_gameover->play();
	sf::sleep(sf::milliseconds(3000)); 
}

void suicide(int* state, Sol sol[11], Cloud cloud[3], Obstacle* o, Blob* b, Menu* m, sf::Sound* sound_gameover, int* NB_SOL, sf::Sprite* s_background, sf::Sprite* s_gameover, sf::Text* text)
{
	*state = 0;
	jspeeed = -16;
	speeed = 4.5;
	window.clear();
	window.draw(*s_background);
	for (int i = 0; i < *NB_SOL; i++ ){sol[i].draw();}
	for (int i = 0; i < 3; i++ ){cloud[i].draw();}
	o->draw();
	b->setState(2);
	b->update();
	window.draw(*text);
	window.draw(*s_gameover);
	window.display();
	m->Reset();
	sound_gameover->play();
	sf::sleep(sf::milliseconds(3000)); 
}

void update(string* s_score, Sol sol[11], Cloud cloud[3], Obstacle* o, Blob* b, sf::Sprite* s_background, sf::Text* text, sf::Color* color, int* score, int* NB_SOL)
{
	*s_score = "Score: " + std::to_string(*score);
	window.clear();
	window.draw(*s_background);
	for (int i = 0; i < *NB_SOL; i++ ){sol[i].update();}
	for (int i = 0; i < 3; i++ ){cloud[i].update();}
	o->update();
	b->update();
	// choix de la chaîne de caractères à afficher
	text->setString(*s_score);
	text->setCharacterSize(12);
	text->setFillColor(*color);
	window.draw(*text);
	window.display();
}

void check_collide(Blob* b, Obstacle* o)
{
	if(b->getState() == 0) //debout
	{
		if(o->getType() == 0)
		{
			if(Collision::PixelPerfectTest(b->s_blob, o->s_small))

			{
				b->setState(2);
			}
		}
		else if(o->getType() == 1)
		{
			if(Collision::PixelPerfectTest(b->s_blob,o->s_large))
			{
				b->setState(2);
			}
		}
		else if(o->getType() == 2)
		{
			if(Collision::PixelPerfectTest(b->s_blob, o->s_ghost))
			{
				b->setState(2);
			}
		}
	}

	else if(b->getState() == 1) //accroupi
	{
		if(o->getType() == 0)
		{
			if(Collision::PixelPerfectTest(b->s_blob_crouch, o->s_small))
			{
				b->setState(2);
			}
		}
		else if(o->getType() == 1)
		{
			if(Collision::PixelPerfectTest(b->s_blob_crouch, o->s_large))
			{
				b->setState(2);
			}
		}
		else if(o->getType() == 2)
		{
			if(Collision::PixelPerfectTest(b->s_blob_crouch, o->s_ghost))
			{
				b->setState(2);
			}
		}
	}
}

void init(int* NB_SOL, Sol sol[11], sf::Font* font, sf::Text* text, sf::Texture* t_background, sf::Sprite* s_background, sf::Texture* t_gameover, sf::Sprite* s_gameover, sf::Music* theme, sf::SoundBuffer* buffer_select, sf::Sound* sound_select, sf::SoundBuffer* buffer_validate,sf::Sound* sound_validate, sf::SoundBuffer* buffer_gameover, sf::Sound* sound_gameover, sf::SoundBuffer* buffer_jump, sf::Sound* sound_jump)
{
	font->loadFromFile("images/pixelmix_bold.ttf");
	text->setFont(*font); 
	text->setPosition(200,10);
	
	t_background->loadFromFile("images/fond_vert.png");
	s_background->setTexture(*t_background);
	s_background->setPosition(0, 0);

	t_gameover->loadFromFile("images/game over gameboy.png");
	s_gameover->setTexture(*t_gameover);
	s_gameover->setPosition(50, 90);

	window.setVerticalSyncEnabled(false);
	window.setFramerateLimit(30);
	window.setKeyRepeatEnabled(false);
	window.setMouseCursorVisible(false);

	theme->openFromFile("Musiques/8bit.wav");
	theme->play();
	theme->setLoop(true);

	buffer_select->loadFromFile("Musiques/sfxMenuScarebotSelect.wav");
	sound_select->setBuffer(*buffer_select);

	buffer_validate->loadFromFile("Musiques/sfxMenuScarebotValidate.wav");
	sound_validate->setBuffer(*buffer_validate);
	
	buffer_gameover->loadFromFile("Musiques/sfxScarebotGameOver.wav");
	sound_gameover->setBuffer(*buffer_gameover);

	
	buffer_jump->loadFromFile("Musiques/sfxBlobRunn3rJump.wav");
	sound_jump->setBuffer(*buffer_jump);

	//on écarte chaque sol de 33px
	for (int i = 1; i < *NB_SOL; i++ )
	{
		sol[i].setX((sol[i-1].getX())+33);
	} //on écarte chaque sol de 33px
}


int main()
{
	string s_score;
	sf::Font font;
	sf::Text text;
	sf::Color color(48, 98, 48);
	sf::Texture t_background;
	sf::Sprite s_background;
	sf::Texture t_gameover;
	sf::Sprite s_gameover;

	int score = 0;
	bool stopjump = false;
	bool jump = false;
	int state = 0; //Etat : 0 = menu. 1 = jeu

	sf::Music theme;
	sf::SoundBuffer buffer_select;
	sf::Sound sound_select;
	sf::SoundBuffer buffer_validate;
	sf::Sound sound_validate;	
	sf::SoundBuffer buffer_gameover;
	sf::Sound sound_gameover;
	sf::SoundBuffer buffer_jump;
	sf::Sound sound_jump;

	Menu m;
	Blob b;
	int NB_SOL = ceil(xwin/33)+2; //11 si xwin = 313
	Sol sol[NB_SOL]; //Tableau de 11 sols (11*33 = nombre minimum pour remplir xwin
	Obstacle o;
	Cloud cloud[3]; //tableau de 3 Nuages
	init(&NB_SOL, sol, &font, &text, &t_background, &s_background, &t_gameover, &s_gameover, &theme, &buffer_select, &sound_select, &buffer_validate, &sound_validate, &buffer_gameover, &sound_gameover, &buffer_jump, &sound_jump);
	
	while (window.isOpen())
	{
		sf::Event event;
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
								score = 0;
								b.Reset();
								o.Reset();
								for (int i = 0; i < NB_SOL; i++ ){sol[i].Reset();}
								for (int i = 0; i < 3; i++ ){cloud[i].Reset();}
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

		else
		{
			if(b.getState()==2)
			{
				death(&state, sol, cloud, &o, &b, &m, &sound_gameover, &NB_SOL, &s_background, &s_gameover, &text);
			}
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
								suicide(&state, sol, cloud, &o, &b, &m, &sound_gameover, &NB_SOL, &s_background, &s_gameover, &text);
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
				update(&s_score, sol, cloud, &o, &b, &s_background, &text, &color, &score, &NB_SOL);
				check_collide(&b, &o);
			}
		}

	}

	return 0;
}