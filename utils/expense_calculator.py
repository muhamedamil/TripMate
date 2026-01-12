#Class calculator

class Calculator:
    @staticmethod
    def multiply(a: int, b: int) -> int:
        """Multiply two integers

        Args:
            a (int): first integer
            b (int): second integer

        Returns:
            int:the product of a and b
        """
        return a*b
        
    @staticmethod
    def calculate_total(*x: float) -> float:
        """Calculate sum of the given list of numbers

        Args:
            X(list): List of floating numbers
        Returns:
            float: The sum of numbers in the list X
        """
        return sum(x)
    
    @staticmethod
    def calculate_daily_budget(total: float, days: int) -> float:
        """Calculate the daily budget 

        Args:
            total (float): Total cost
            days (int): Total days

        Returns:
            float: Expense for the single day
        """
        return total / days if days > 0 else 0 
        