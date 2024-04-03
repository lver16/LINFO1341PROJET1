from agent import Agent
import random
from shobu import ShobuGame, ShobuState, ShobuAction
class AI(Agent):
    """An agent that uses the alpha-beta pruning algorithm to determine the best move.

    This agent extends the base Agent class, providing an implementation of the play
    method that utilizes the alpha-beta pruning technique to make decisions more efficiently.

    Attributes:
        max_depth (int): The maximum depth the search algorithm will explore.
    """

    def __init__(self, player, game, max_depth=30):
        """Initializes an AlphaBetaAgent instance with a specified player, game, and maximum search depth.

        Args:
            player (int): The player ID this agent represents (0 or 1).
            game (ShobuGame): The Shobu game instance the agent will play on.
            max_depth (int): The maximum depth of the search tree.
        """
        super().__init__(player, game)
        self.max_depth = max_depth
        self.table_transposition = self.init_table_zobrist()
        self.historique = {}
        self.count = 0
        self.quiescence_depth_limit = max_depth 
        self.killer_moves = {depth: [None, None] for depth in range(max_depth)}


    def play(self, state, remaining_time):
        """Determines the best action by applying the alpha-beta pruning algorithm.

        Overrides the play method in the base class.

        Args:
            state (ShobuState): The current state of the game.
            remaining_time (float): The remaining time in seconds that the agent has to make a decision.

        Returns:
            ShobuAction: The action determined to be the best by the alpha-beta algorithm.
        """
        
        actions = self.game.actions(state)
        if len(actions) == 1:
            return actions[0]
        for a in actions:
            if self.game.result(state, a).utility == 1:
                return a
            
        # diff_max = -float("inf")
        # id_max = 0
        #trier les actions en mettant uniquement les actions ou le active board a un nombre de pions adverses plus petit que le notre
        # for index, b in enumerate(state.board):
        #     plat_player = list(b[self.player])
        #     plat_opp = list(b[1-self.player])
        #     diff = len(plat_player) - len(plat_opp)
        #     if diff > diff_max:
        #         diff_max = diff
        #         id_max = index
        # actions = [a for a in actions if a.active_board_id == id_max or a.passive_board_id == id_max]
        if self.player == 0:
            plateau_player = [0, 1]
            plateau_opp = [2, 3]
            stone_player_passive = [0, 3]
            direction = [5, 3]
            
        else:
            plateau_player = [2, 3]
            plateau_opp = [0, 1]
            stone_player_passive = [12, 15]
            direction = [-3, -5]
        
        #pour commencer la partie, on place les pions extérieurs dans le centre pour former un bloc
        if self.count <=1:            
            liste_to_do = []
            for i in plateau_player:
                for j in plateau_opp:
                    # liste_to_do.append(ShobuAction(i, 0, j, 0, 5, 1))
                    # liste_to_do.append(ShobuAction(i, 3, j, 3, 3, 1))
                    
                    # liste_to_do.append(ShobuAction(i, 12, j, 12, -3, 1))
                    # liste_to_do.append(ShobuAction(i, 15, j, 15, -5, 1))
                    
                    liste_to_do.append(ShobuAction(i, stone_player_passive[0], j, stone_player_passive[0], direction[0], 1))
                    liste_to_do.append(ShobuAction(i, stone_player_passive[1], j, stone_player_passive[1], direction[1], 1))
            for a in liste_to_do:
                if a in actions:
                    return a      
            #         
            # if self.player == 0:
            #     liste_to_do.append(ShobuAction(0, 0, 2, 0, 5, 1))
            #     liste_to_do.append(ShobuAction(1, 0, 3, 0, 4, 1))
                
            #     liste_to_do.append(ShobuAction(0, 3, 2, 3, 3, 1))
            #     liste_to_do.append(ShobuAction(1, 3, 3, 3, 4, 1))
            # else:
            #     liste_to_do.append(ShobuAction(2, 12, 0, 12, -4, 1))
            #     liste_to_do.append(ShobuAction(3, 12, 1, 12, -4, 1))
                
            #     liste_to_do.append(ShobuAction(2, 15, 0, 15, -4, 1))


            
        #avant les 4 premiers coups, si on peut capturer une piece on le fait
        elif self.count < 4 and self.count > 1:
            liste_decision = []
            for a in actions:
                if self.tej_pion(state, a):
                    
                    liste_decision.append(a)
            if len(liste_decision) > 0:
                for a in liste_decision:
                    if a.active_stone_id not in [12, 15, 0, 3]:
                        return a
 
        
        
            
        self.count += 1
            
        depth_limit = 5
        self.quiescence_depth_limit = depth_limit -1
        depths = range(1, depth_limit + 1)
        

        best_action = None  
        best_val = float("-inf")
        for depth in depths:
            self.max_depth = depth
            score, action = self.max_value(state, -float("inf"), float("inf"), 0)
            if score > best_val:
                best_val = score
                best_action = action
                
        # best_action = self.alpha_beta_search(state)
        return best_action
        
            
    def tej_pion(self, old_state, move):
        new_state = self.game.result(old_state, move)
        old_board = old_state.board
        new_board = new_state.board
        new_count_player = [0, 0, 0, 0]
        new_count_opp = [0, 0, 0, 0]
        old_count_player = [0, 0, 0, 0]
        old_count_opp= [0, 0, 0, 0]
        
        plateau_active = move.active_board_id
        new_count_opp[plateau_active] += len(new_board[plateau_active][1-self.player])
        new_count_player[plateau_active] += len(new_board[plateau_active][self.player])
        old_count_opp[plateau_active] += len(old_board[plateau_active][1-self.player])
        old_count_player[plateau_active] += len(old_board[plateau_active][self.player])
        
        n = old_count_opp[plateau_active] - new_count_opp[plateau_active]
        if n > 0:
            return True
        return False
        
    
    def is_cutoff(self, state, depth):
        """Determines if the search should be cut off at the current depth.

        Args:
            state (ShobuState): The current state of the game.
            depth (int): The current depth in the search tree.

        Returns:
            bool: True if the search should be cut off, False otherwise.
        """

    
        return self.game.is_terminal(state) or depth == self.max_depth
    
    
        
    
    def eval_basic(self, state):
        """Evaluates the given state and returns a score from the perspective of the agent's player.

        Args:
            state (ShobuState): The game state to evaluate.

        Returns:
            float: The evaluated score of the state.
        """
        score = 0
        my_player = self.game.to_move(state)
        mini_blanc = float("inf")
        mini_noir = float("inf")
        board = state.board
        for b in board:  #vérifie 1 plateau à la fois
            
            #récupère la nombre de pièce appartenant à chaque joueur
            nombre_piece_blanc = len(b[0])
            nombre_piece_noir = len(b[1])
            
            mini_blanc = min(mini_blanc, nombre_piece_blanc)
            mini_noir = min(mini_noir, nombre_piece_noir)
            
        if(my_player == 0): #mon joueur joue les pieces blanches
            score += mini_blanc - mini_noir
        else: #mon joueur joue les pieces noires
            score += mini_noir - mini_blanc
            
        return score
    
    


    def alpha_beta_search(self, state):
        """Implements the alpha-beta pruning algorithm to find the best action.

        Args:
            state (ShobuState): The current game state.

        Returns:
            ShobuAction: The best action as determined by the alpha-beta algorithm.
        """
        _, action = self.max_value(state, -float("inf"), float("inf"), 0)
        return action
    
    

    def pion(self, state, old_state, move):
        new_board = state.board
        old_board = old_state.board
        
        new_count_player = [0, 0, 0, 0]
        new_count_opp = [0, 0, 0, 0]
        old_count_player = [0, 0, 0, 0]
        old_count_opp= [0, 0, 0, 0]

        
        plateau_active = move.active_board_id
        new_count_opp[plateau_active] += len(new_board[plateau_active][1-self.player])
        new_count_player[plateau_active] += len(new_board[plateau_active][self.player])
        old_count_opp[plateau_active] += len(old_board[plateau_active][1-self.player])
        old_count_player[plateau_active] += len(old_board[plateau_active][self.player])
        
        plateau_passive = move.passive_board_id
        new_count_opp[plateau_passive] += len(new_board[plateau_passive][1-self.player])
        new_count_player[plateau_passive] += len(new_board[plateau_passive][self.player])
        old_count_opp[plateau_passive] += len(old_board[plateau_passive][1-self.player])
        old_count_player[plateau_passive] += len(old_board[plateau_passive][self.player])
        
        nombre_pion_adverse_en_moins = old_count_opp[plateau_active] - new_count_opp[plateau_active]
        nombre_pion_adverse_en_moins += old_count_opp[plateau_passive] - new_count_opp[plateau_passive]
        
        if old_count_opp[plateau_active] - new_count_opp[plateau_active] > 0:
            nombre_pion_adverse_en_moins += 0.5
        if old_count_opp[plateau_passive] - new_count_opp[plateau_passive] > 0:
            nombre_pion_adverse_en_moins += 0.25
        return nombre_pion_adverse_en_moins
    

    
    def nombre_pion_ciao(self, state, play):
        ai = AI(1-play, self.game)
        actions = ai.game.compute_actions(state.board, play)
        count = 0
        for a in actions:
            old = state
            new = self.game.result(state, a)
            if self.pion(new, old, a ) > 0:
                count += 1
        return count/24
    
    def heuristique1_lucas(self, state):
        board = state.board
        score = 0
        
        white = [0, 1]
        black = [2, 3]
        if self.player == 0:
            player = white
            opp = black
        else:
            player = black
            opp = white
        
        for index,b in enumerate(board):
            player_piece = (b[self.player])
            opponent_piece = (b[1-self.player])
            if len(player_piece) == 0:
                return 0
            if len(opponent_piece) == 0:
                return 1
            
            if len(player_piece) == 4:
                if index in player:
                    score += 40
                else:
                    score += 30
                    
            elif len(player_piece) == 3:
                if index in player:
                    score += 30
                else:
                    score += 20
                    
            elif len(player_piece) == 2:
                if index in player:
                    score += 5
                else:
                    score += 5
      
            elif len(player_piece) == 1:
                if index in player:
                    score += 0
                else:
                    score += 0
                    
            if len(opponent_piece) == 4:
                score -= 45
            elif len(opponent_piece) == 3:
                score -= 15
            elif len(opponent_piece) == 2:
                score -= 5
            elif len(opponent_piece) == 1:
                score += 10
                
        return score/4/40
    
    def heuristique2_fastghost(self, state):
        if (state.utility == 1 and self.player == 0) or (state.utility == -1 and self.player == 1) :
            return 1
        elif (state.utility == 1 and self.player == 1) or (state.utility == -1 and self.player == 0) :
            return 0
        countM = [0, 0, 0, 0, 0]
        countY = [0, 0, 0, 0, 0]
        for row in state.board:
            if self.player == 0 :
                countM[len(row[0])] += 1
                countY[len(row[1])] += 1
            else :
                countM[len(row[1])] += 1
                countY[len(row[0])] += 1
        if countM[0] > 0:
            return 0
        if countY[0] > 0:
            return 1
        result = 0.5 + ((countY[1]-countM[1])* 0.1) + ((countY[2]-countM[2])* 0.03) + ((countY[3]-countM[3])* 0.008) + ((countY[4]-countM[4])* 0.002)
        return result     
        
    def heuristique3_centre(self, state):
        centre = [5, 6, 9, 10]
        score = 0
        for b in state.board:
            for s in b[self.player]:
                if s in centre:
                    score += 1
            for s in b[1-self.player]:
                if s in centre:
                    score -= 1
        return score/16
    
    def heuristique4_insertion_entre_2pions(self, state):
        limite_droite = [3, 7, 11, 15]  
        limite_gauche = [0, 4, 8, 12]
        limite_haute = [12, 13, 14, 15]
        limite_basse = [0, 1, 2, 3]
        
        white = [0, 1]
        black = [2, 3]
        
        if self.player == 0:
            player = white
            opp = black
        else:
            player = black
            opp = white
        
        
        score = 0
        board = state.board
        for index, b in enumerate(board):
            # if index in player:
            plateau_player = list(b[self.player])
            plateau_opp = list(b[1-self.player])
            for i in range(len(plateau_player)):
                #regarde si un pion à nous se trouve entre 2 pions adverses sur le plateau
                
                #par rapport aux lignes
              
                if plateau_player[i] not in limite_droite and plateau_player[i] not in limite_gauche:
                    if plateau_player[i] + 1 in plateau_opp and plateau_player[i] - 1 in plateau_opp:
                        score += 1
                #par rapport aux colonnes
                if plateau_player[i] not in limite_haute and plateau_player[i] not in limite_basse:
                    if plateau_player[i] + 4 in plateau_opp and plateau_player[i] - 4 in plateau_opp:
                        score += 1
                        
                #par rapport à la diagonale
                if plateau_player[i] not in limite_haute and plateau_player[i] not in limite_droite and plateau_player[i] not in limite_gauche and plateau_player[i] not in limite_basse:
                    if plateau_player[i] + 3 in plateau_opp and plateau_player[i] - 3 in plateau_opp:
                        score += 1
                    if plateau_player[i] + 5 in plateau_opp and plateau_player[i] - 5 in plateau_opp:
                        score += 1
        return score/16
    
    def heursitique5_mobilite_home_board(self, state):
        board = state.board
        score = 0
        white = [0, 1]
        black = [2, 3]
        
        if self.player == 0:
            player = white
            opp = black
        else:
            player = black
            opp = white
            
        actions = self.game.actions(state)

        score += len(actions)
        return score/24


    def heuristique6_kill_pion_adverse(self, state, old_state, move):
        new_board = state.board
        old_board = old_state.board
        
        new_count_player = [0, 0, 0, 0]
        new_count_opp = [0, 0, 0, 0]
        old_count_player = [0, 0, 0, 0]
        old_count_opp= [0, 0, 0, 0]

        
        plateau_active = move.active_board_id
        new_count_opp[plateau_active] += len(new_board[plateau_active][1-self.player])
        new_count_player[plateau_active] += len(new_board[plateau_active][self.player])
        old_count_opp[plateau_active] += len(old_board[plateau_active][1-self.player])
        old_count_player[plateau_active] += len(old_board[plateau_active][self.player])
        
        
        nombre_pion_adverse_en_moins = old_count_opp[plateau_active] - new_count_opp[plateau_active]
        
        actions = self.game.actions(state)

        for a in actions:
            plateau_active_opp = a.active_board_id
            new_state = self.game.result(state, a)
            c_opp =[0, 0, 0, 0]
            c_opp[plateau_active_opp] += len(new_state.board[plateau_active_opp][self.player])
            diff = old_count_player[plateau_active_opp] - c_opp[plateau_active_opp]
            if diff > 0:
                nombre_pion_adverse_en_moins -=1
        
        
        return nombre_pion_adverse_en_moins
    
    def heuristique7_kill_pion(self, state, old_state, move):
        old_board = old_state.board
        new_board = state.board
        new_count_player = [0, 0, 0, 0]
        new_count_opp = [0, 0, 0, 0]
        old_count_player = [0, 0, 0, 0]
        old_count_opp= [0, 0, 0, 0]
        
        id_active = move.active_board_id
        new_count_opp[id_active] += len(new_board[id_active][1-self.player])
        new_count_player[id_active] += len(new_board[id_active][self.player])
        old_count_opp[id_active] += len(old_board[id_active][1-self.player])
        old_count_player[id_active] += len(old_board[id_active][self.player])
        
        capture_piece = old_count_opp[id_active] - new_count_opp[id_active]
        
        return capture_piece
    
    def heurisitque8_kill_pion_safe(self, state, old_state, move):
        new_board = state.board
        old_board = old_state.board
        score = 0
        
        new_count_player = [0, 0, 0, 0]
        new_count_opp = [0, 0, 0, 0]
        old_count_player = [0, 0, 0, 0]
        old_count_opp= [0, 0, 0, 0]

        
        plateau_active = move.active_board_id
        new_count_opp[plateau_active] += len(new_board[plateau_active][1-self.player])
        new_count_player[plateau_active] += len(new_board[plateau_active][self.player])
        old_count_opp[plateau_active] += len(old_board[plateau_active][1-self.player])
        old_count_player[plateau_active] += len(old_board[plateau_active][self.player])

        nombre_pion_adverse_en_moins = old_count_opp[plateau_active] - new_count_opp[plateau_active]

        if nombre_pion_adverse_en_moins == 1:
            id_capture = move.active_stone_id
            limite_droite = [3, 7, 11, 15]  
            limite_gauche = [0, 4, 8, 12]
            limite_haute = [12, 13, 14, 15]
            limite_basse = [0, 1, 2, 3]
            
            white = [0, 1]
            black = [2, 3]
            
            if self.player == 0:
                player = white
                opp = black
            else:
                player = black
                opp = white
            

            #regarde si un pion à nous se trouve entre 2 pions adverses sur le plateau
            
            #par rapport aux lignes
            
            plateau_player = list(new_board[plateau_active][self.player])
            plateau_opp = list(new_board[plateau_active][1-self.player])
        
            if id_capture not in limite_droite and id_capture not in limite_gauche:
                if (id_capture + 1 in plateau_opp and id_capture - 1 in plateau_opp) or (id_capture + 1 in plateau_opp and id_capture - 1 in plateau_player) or (id_capture + 1 in plateau_player and id_capture - 1 in plateau_opp) or (id_capture + 1 in plateau_player and id_capture - 1 in plateau_player):
                    score += 1
            #par rapport aux colonnes
            if id_capture not in limite_haute and id_capture not in limite_basse:
                if (id_capture + 4 in plateau_opp and id_capture - 4 in plateau_opp) or (id_capture + 4 in plateau_opp and id_capture - 4 in plateau_player) or (id_capture + 4 in plateau_player and id_capture - 4 in plateau_opp) or (id_capture + 4 in plateau_player and id_capture - 4 in plateau_player):
                    score += 1
                    
            #par rapport à la diagonale
            if id_capture not in limite_haute and id_capture not in limite_droite and id_capture not in limite_gauche and id_capture not in limite_basse:
                if (id_capture + 3 in plateau_opp and id_capture - 3 in plateau_opp) or (id_capture + 3 in plateau_opp and id_capture - 3 in plateau_player) or (id_capture + 3 in plateau_player and id_capture - 3 in plateau_opp) or (id_capture + 3 in plateau_player and id_capture - 3 in plateau_player):
                    score += 1
                if (id_capture + 5 in plateau_opp and id_capture - 5 in plateau_opp) or (id_capture + 5 in plateau_opp and id_capture - 5 in plateau_player) or (id_capture + 5 in plateau_player and id_capture - 5 in plateau_opp) or (id_capture + 5 in plateau_player and id_capture - 5 in plateau_player):
                    score += 1
                
        return score
    
    def heuristique9_kill_ou_il_y_moins_de_pion(self, state, old_state, move):
        old_board = old_state.board
        new_board = state.board
        new_count_player = [0, 0, 0, 0]
        new_count_opp = [0, 0, 0, 0]
        old_count_player = [0, 0, 0, 0]
        old_count_opp= [0, 0, 0, 0]
        
        for index, b in enumerate(old_board):
            old_count_opp[index] += len(b[1-self.player])
            old_count_player[index] += len(b[self.player])
        
        for index, b in enumerate(new_board):
            new_count_opp[index] += len(b[1-self.player])
            new_count_player[index] += len(b[self.player])
        
        id_active = move.active_board_id
        
        capture_piece = old_count_opp[id_active] - new_count_opp[id_active]
        
        if capture_piece > 0:
            val = float("inf")
            ind = 0
            for i in range(4):
                if new_count_opp[i] < val:
                    val = new_count_opp[i]
                    ind = i
            if ind == id_active:
                return 1
            else:
                return 0
        return 0
    
    def heuristique10_count_plateau(self, state):
        board = state.board
        score = 0
        count_player = [0, 0, 0, 0]
        count_opp = [0, 0, 0, 0]
        for index, b in enumerate(board):
            count_player[index] += len(b[self.player])
            count_opp[index] += len(b[1-self.player])
        white = [0, 1]
        black = [2, 3]
        if self.player == 0:
            player = white
            opp = black
        else:
            player = black
            opp = white
        
        for i in opp:
            if count_player[i] >=3 :
                score += 1
            if count_opp[i] < 3:
                score += 1
        for i in player:
            if count_opp[i] == 3 :
                score += 1
            if count_player[i] < 3:
                score += 1
        return score/8
    def heuristique(self, state, old_state, move):
        
        n_opp = self.pion(state, old_state, move)
        #nombre_pion_opp_eject = self.nombre_pion_ciao(state, 1-self.player)
        h1 = self.heuristique1_lucas(state)
        h2 = self.heuristique2_fastghost(state)
        h3 = self.heuristique3_centre(state)
        h4 = self.heuristique4_insertion_entre_2pions(state)
        h5 = self.heursitique5_mobilite_home_board(state)
        h6 = self.heuristique6_kill_pion_adverse(state, old_state, move)
        h7 = self.heuristique7_kill_pion(state, old_state, move)
        h8 = self.heurisitque8_kill_pion_safe(state, old_state, move)
        h9 = self.heuristique9_kill_ou_il_y_moins_de_pion(state, old_state, move)
        h10 = self.heuristique10_count_plateau(state)
        if (state.utility == 1 and self.player == 0) or (state.utility == -1 and self.player == 1) :
            return (1, None)
        elif (state.utility == 1 and self.player == 1) or (state.utility == -1 and self.player == 0) :
            return (0, None)
        
        #score = h1*0.1+ h2*0.9 + h3*0.001 + h4*0.5
        
        #score = (h4*0.1 + 0.25*h3) + (0.45*h1 + 0.45*h2)  + h5*0.001 + h6*0.05
        
        pond_h1 = 0.15
        pond_h2 = 0.45
        pond_h3 = 0.25
        pond_h4 = 0.1
        pond_h5 = 0.001
        pond_h6 = 0.05
        pond_h7 = 0.1
        pond_h8 = 0.8
        #score = pond_h7*h7 + (pond_h1*h1 + pond_h2*h2) + (pond_h4*h4 + pond_h3*h3)  + pond_h5*h5 + pond_h6*h6
        # BEST SCORE score = h2*0.6 + h1*0.3 + (h8*0.05 + 0.05*h3) + h5*0.005 
        score = h2*0.6 + h1*0.3 + h8*0.05 + 0.05*h3 + h5*0.005
        
        #h3 et h5 à 0.01 gagne en tant que noir
        #h3 == 0.05 et h5 == 0.001 gagne en tant que blanc
        #score = h2*0.6 + h1*0.3 + (h8*0.05 + 0.05*h3) + h5*0.005 GAGNE CONTRE MEDIUM BLANC ET NOIR
        
        #h1 20/30%, h2 20/30%, h3 10/15%, h4 10/15%, h5 20/30%

        
        
        return  (score, None)
    

    def max_value(self, state, alpha, beta, depth,  old_state = None, move=None):
        """Computes the maximum achievable value for the current player at a given state using the alpha-beta pruning.

        This method recursively explores all possible actions from the current state to find the one that maximizes
        the player's score, pruning branches that cannot possibly affect the final decision.

        Args:
            state (ShobuState): The current state of the game.
            alpha (float): The current alpha value, representing the minimum score that the maximizing player is assured of.
            beta (float): The current beta value, representing the maximum score that the minimizing player is assured of.
            depth (int): The current depth in the search tree.

        Returns:
            tuple: A tuple containing the best value achievable from this state and the action that leads to this value.
                If the state is a terminal state or the depth limit is reached, the action will be None.
        """
        
        if(self.is_cutoff(state, depth)):
            return self.heuristique(state, old_state, move)
        
       

            
        v = float("-inf")
        action = None
        actions = self.game.actions(state)
        #actions = self.trie_actions(state, actions)
        #actions = sorted(actions, key = lambda x: self.heuristique(self.game.result(state, x), state, x)[0], reverse=True)
        #actions = sorted(actions, key = lambda x: self.heuristique(self.game.result(state, x), state, x)[0], reverse=True)


                
        for a in actions:
            new_hash = self.calculate_new_hash(state, a)
            if new_hash not in self.historique:
                v2, a2 = self.min_value(self.game.result(state, a), alpha, beta, depth + 1, state, a)
                self.historique[new_hash] = (v2, a2)
            
            else:
                v2, a2 = self.historique[new_hash]
                
            #v2, a2 = self.min_value(self.game.result(state, a), alpha, beta, depth + 1)  
            if(v2 > v):
                v = v2
                action = a
                alpha = max(alpha, v)
            if(v >= beta):

                return v, action

        return v, action
    
    def trie_actions(self, state, actions):
        a_garder = []
        for a in actions:
            new_state = self.game.result(state, a)
            actions_opp = self.game.actions(new_state)
            for a_opp in actions_opp:
                state_opp = self.game.result(new_state, a_opp)
                count_player_old = [0, 0, 0, 0]
                count_opp_old = [0, 0, 0, 0]
                count_player_new = [0, 0, 0, 0]
                count_opp_new = [0, 0, 0, 0]
                for index, b in enumerate(new_state.board):
                    count_player_old[index] += len(b[self.player])
                    count_opp_old[index] += len(b[1-self.player])
                for index, b in enumerate(state_opp.board):
                    count_player_new[index] += len(b[self.player])
                    count_opp_new[index] += len(b[1-self.player])
                active_id_opp = a_opp.active_board_id
                if count_player_old[active_id_opp] - count_player_new[active_id_opp] == 0:
                    a_garder.append(a)
                    
                    
        return a_garder
                
            


    def min_value(self, state, alpha, beta, depth, old_state = None, move=None):
        """Computes the minimum achievable value for the opposing player at a given state using the alpha-beta pruning.

        Similar to max_value, this method recursively explores all possible actions from the current state to find
        the one that minimizes the opponent's score, again using alpha-beta pruning to cut off branches that won't
        affect the outcome.

        Args:
            state (ShobuState): The current state of the game.
            alpha (float): The current alpha value, representing the minimum score that the maximizing player is assured of.
            beta (float): The current beta value, representing the maximum score that the minimizing player is assured of.
            depth (int): The current depth in the search tree.

        Returns:
            tuple: A tuple containing the best value achievable from this state for the opponent and the action that leads to this value.
                If the state is a terminal state or the depth limit is reached, the action will be None.
        """
        if(self.is_cutoff(state, depth)):
            return self.heuristique(state, old_state, move)
        
        v = float("inf")
        action = None
        actions = self.game.actions(state)
        #actions = self.trie_actions(state, actions)
        #actions = sorted(actions, key = lambda x: self.heuristique(self.game.result(state, x), state, x)[0])
        #actions = sorted(actions, key = lambda x: self.heuristique(self.game.result(state, x), state, x)[0])


        for a in actions:
            new_hash = self.calculate_new_hash(state, a)
            if new_hash not in self.historique :
                v2, a2 = self.max_value(self.game.result(state, a), alpha, beta, depth + 1, state, a)
                self.historique[new_hash] = (v2, a2)
            
            else:
                v2, a2 = self.historique[new_hash]
            if(v2 < v):
                v = v2
                action = a
                beta = min(beta, v)
            if(v <= alpha):

                return v, action
            

        return v, action
    
    def is_stable(self, state, old_state, move):
        actions_futurs = self.game.actions(state)
        for a in actions_futurs:
            new_state = self.game.result(state, a)
            score_old = self.heuristique(state, old_state, move)
            score_new = self.heuristique(new_state, state, a)
            if abs(score_old[0] - score_new[0]) > 0.1:
                return False
        return True
    
    def quiescence_search(self, state, old_state, move, alpha, beta, depth):
        """Performs a quiescence search to handle unstable positions."""
        # Perform a quiescence search until a stable position is reached

        v = self.heuristique(state, old_state, move)[0]
        if v >= beta:
            return beta, None  # Cutoff

        if alpha < v:
            alpha = v

        # Consider capturing moves and other critical actions
        for a in self.game.actions(state):
            new_state = self.game.result(state, a)
            score = self.heuristique(new_state, old_state, move)[0]
            v = max(v, score)

            if v >= beta:
                return beta, None  # Cutoff

            if alpha < v:
                alpha = v

        return v, None
            
    def init_table_zobrist(self):
        keys = {}
        all_types_of_pieces = [0, 1]
        for plateau in range(4):
            for case in range(16):
                for piece in all_types_of_pieces:
                    keys[plateau, case, piece] = random.getrandbits(64)
    
        return keys
    
    def calculate_hash(self, state):
        hash = 0
        board = state.board
        for plateau in range(4):
            for index, color in enumerate(board[plateau]):  #color représente les positions des pièces blanches puis noires
                for position in color:
                    hash ^= self.table_transposition[plateau, position, index]
        
        return hash
    
    def calculate_new_hash(self, state, action):
        old_hash = self.calculate_hash(state)
        move_passive = self.table_transposition[action.passive_board_id, action.passive_stone_id, self.game.to_move(state)]
        move_active = self.table_transposition[action.active_board_id, action.active_stone_id, self.game.to_move(state)]
        new_hash = old_hash ^ move_passive ^ move_active
  
        return new_hash