# first parent
class Father:
    def skill1(self):
        print("Driving")


# second parent
class Mother:
    def skill2(self):
        print("Cooking")


# child inherits from both
class Child(Father, Mother):
    pass


c = Child()
c.skill1()
c.skill2()
