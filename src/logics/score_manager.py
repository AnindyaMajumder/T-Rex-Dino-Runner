import os
import json
import time

class ScoreManager:
    def __init__(self, file_path="high_score.json"):
        self.file_path = file_path
        self.last_save_time = time.time()  # Initialize this attribute first
        self.save_cooldown = 2.0  # Only save every 2 seconds to avoid excessive writes
        self.high_score = self.load_high_score()
        self.score_history = self.load_score_history()
    
    def load_high_score(self):
        """Load high score from file"""
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r') as file:
                    content = file.read().strip()
                    if content:  # Check if file is not empty
                        data = json.loads(content)
                        return data.get('high_score', 0)
        except Exception as e:
            print(f"Error loading high score: {e}")
            # Create the file if it doesn't exist or is corrupt
            try:
                self.save_high_score(0, force=True)
            except Exception as e2:
                print(f"Error creating high score file: {e2}")
        return 0
    
    def load_score_history(self):
        """Load score history from file"""
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r') as file:
                    content = file.read().strip()
                    if content:  # Check if file is not empty
                        data = json.loads(content)
                        return data.get('score_history', [])
        except Exception as e:
            print(f"Error loading score history: {e}")
        return []
        
    def save_high_score(self, score, force=False):
        """Save high score to file if it's higher than the current one"""
        current_time = time.time()
        
        # Check cooldown to avoid excessive writes
        if not force and current_time - self.last_save_time < self.save_cooldown:
            return
            
        self.last_save_time = current_time
        
        if score > self.high_score:
            self.high_score = score
            
            # Add the new high score to history with timestamp
            entry = {
                'score': score,
                'date': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Initialize history if needed
            if not hasattr(self, 'score_history') or self.score_history is None:
                self.score_history = []
                
            self.score_history.append(entry)
            
            # Keep only the top 10 scores in history
            self.score_history.sort(key=lambda x: x['score'], reverse=True)
            self.score_history = self.score_history[:10]
            
        # Write data to file
        try:
            data = {
                'high_score': self.high_score,
                'score_history': self.score_history if hasattr(self, 'score_history') else [],
                'last_played': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Create directory if it doesn't exist
            directory = os.path.dirname(self.file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
                
            with open(self.file_path, 'w') as file:
                json.dump(data, file, indent=2)
                
            # Create a backup after successful save
            self.create_backup()
        except Exception as e:
            print(f"Error saving high score: {e}")
    
    def get_high_score(self):
        """Get the current high score"""
        return self.high_score
    
    def get_score_history(self):
        """Get the score history"""
        if not hasattr(self, 'score_history') or self.score_history is None:
            self.score_history = []
        return self.score_history
    
    def reset_scores(self):
        """Reset all scores - mostly for testing"""
        self.high_score = 0
        self.score_history = []
        self.save_high_score(0, force=True)
        return True
        
    def create_backup(self):
        """Create a backup of the high score file"""
        if os.path.exists(self.file_path):
            backup_path = f"{self.file_path}.bak"
            try:
                with open(self.file_path, 'r') as src:
                    content = src.read()
                    if content.strip():  # Only backup if file has content
                        with open(backup_path, 'w') as dst:
                            dst.write(content)
                return True
            except Exception as e:
                print(f"Error creating backup: {e}")
        return False

    def restore_from_backup(self):
        """Restore high scores from backup file if main file is corrupted"""
        backup_path = f"{self.file_path}.bak"
        if os.path.exists(backup_path):
            try:
                with open(backup_path, 'r') as src:
                    content = src.read()
                    if content.strip():  # Only restore if backup has content
                        with open(self.file_path, 'w') as dst:
                            dst.write(content)
                # Reload the data
                self.high_score = self.load_high_score()
                self.score_history = self.load_score_history()
                return True
            except Exception as e:
                print(f"Error restoring from backup: {e}")
        return False
        
    def save_score(self, score):
        """Save a score to history even if it's not a high score"""
        try:
            # Add the score to history with timestamp
            entry = {
                'score': score,
                'date': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Initialize history if needed
            if not hasattr(self, 'score_history') or self.score_history is None:
                self.score_history = []
                
            self.score_history.append(entry)
            
            # Keep only the top 10 scores in history
            self.score_history.sort(key=lambda x: x['score'], reverse=True)
            self.score_history = self.score_history[:10]
            
            # Also update high score if needed
            if score > self.high_score:
                self.high_score = score
                
            # Write data to file
            data = {
                'high_score': self.high_score,
                'score_history': self.score_history,
                'last_played': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Create directory if it doesn't exist
            directory = os.path.dirname(self.file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
                
            with open(self.file_path, 'w') as file:
                json.dump(data, file, indent=2)
                
            # Create a backup after successful save
            self.create_backup()
            return True
        except Exception as e:
            print(f"Error saving score: {e}")
            return False