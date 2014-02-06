class Signal : public Item {
public:

void move(x, y);

Q_SIGNALS: void moved(int x, int y); public:

void doSomething();
};
