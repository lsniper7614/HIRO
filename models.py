import numpy as np
import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.nn.functional as F
import torch.nn.init as init

import utils

def var(tensor):
    if torch.cuda.is_available():
        return Variable(tensor).cuda()
    else:
        return Variable(tensor)

class Actor(nn.Module):
    def __init__(self, state_dim, goal_dim, action_dim, max_action):
        super(Actor, self).__init__()

        self.l1 = nn.Linear(state_dim + goal_dim, 400)
        self.l2 = nn.Linear(400, 300)
        self.l3 = nn.Linear(300, action_dim)
        
        self.max_action = max_action
    
    def forward(self, x, g):
        x = F.relu(self.l1(torch.cat([x, g], 1)))
        x = F.relu(self.l2(x))
        x = self.max_action * torch.tanh(self.l3(x)) 
        return x 


class Critic(nn.Module):
    def __init__(self, state_dim, goal_dim, action_dim):
        super(Critic, self).__init__()

        self.l1 = nn.Linear(state_dim + goal_dim + action_dim, 400)
        self.l2 = nn.Linear(400, 300)
        self.l3 = nn.Linear(300, 1)


    def forward(self, x, g, u):
        x = F.relu(self.l1(torch.cat([x, g, u], 1)))
        x = F.relu(self.l2(x))
        x = self.l3(x)
        return x 

class ControllerActor(nn.Module):
    def __init__(self, state_dim, goal_dim, action_dim, max_action=1):
        super(ControllerActor, self).__init__()
        self.actor = Actor(state_dim, goal_dim, action_dim, 1)
    
    def forward(self, x, sg):
        return self.actor(x, sg)


class ControllerCritic(nn.Module):
    def __init__(self, state_dim, goal_dim, action_dim):
        super(ControllerCritic, self).__init__()

        self.critic = Critic(state_dim, goal_dim, action_dim)
    
    def forward(self, x, sg, u):
        return self.critic(x, sg, u)

class ManagerActor(nn.Module):
    def __init__(self, state_dim, goal_dim, action_dim, max_action=1):
        super(ManagerActor, self).__init__()
        # TODO: what is the max action
        self.actor = Actor(state_dim, goal_dim, action_dim, 1)
    
    def forward(self, x, g):
        return self.actor(x, g)


class ManagerCritic(nn.Module):
    def __init__(self, state_dim, goal_dim, action_dim):
        super(ManagerCritic, self).__init__()
        self.critic = Critic(state_dim, goal_dim, action_dim)
    
    def forward(self, x, g, u):
        return self.critic(x, g, u)
