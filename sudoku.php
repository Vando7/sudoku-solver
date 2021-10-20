<?php
	class Sudoku{
		private $board;
		private $path;
		private $do_print;
		

		function __construct($input_path){
			$this->path = $input_path;
			$do_print = false;
			
			$input_file = fopen($input_path,"r") or die("Could not open file.");
			$this->board = array_pad(array(), 10, array());
			
			$char_counter = 0;
			$row_counter = 0;
			
			while(!feof($input_file)){
				if($char_counter == 9){
					$row_counter++;
					$char_counter = 0;
					$trash=fgetc($input_file);
					$trash=fgetc($input_file);
				}
				
				array_push($this->board[$row_counter],fgetc($input_file));
				$char_counter++;
			}
				
			fclose($input_file);
		}
		

		function set_print($value){
			$this->do_print = $value;
		}

		
		function print__board($b){
			for($i=0;$i<9;$i++){
				for($j=0;$j<9;$j++){
					print $b[$i][$j];
					
					if($j==2 || $j==5){
						print " ";
					}
					
					print " ";
				}
				if($i==2 || $i==5){
					print "\n";
				}
				print "\n";
			}
		}


		function print_board(){
			$this->print__board($this->board);
		}
		
		
		function write_board($b){
			$output_path = substr($this->path,0,-4)."-solved.txt";
			$output_file = fopen($output_path,"w");
			
			for($i=0;$i<9;$i++){
				for($j=0;$j<9;$j++){
					fwrite($output_file,$b[$i][$j]);
				}
				fwrite($output_file,"\n");
			}
			
			fclose($output_file);
		}

		
		function possible_values($board,$row,$col){
			$used_values = array_pad(array(), 10,0);
			
			// Check what numbers occupy given row and col
			for($i=0;$i<9;$i++){
				if($board[$i][$col]!=0){
					$used_values[$board[$i][$col]] = 1;
				}
				
				if($board[$row][$i]!=0){
					$used_values[$board[$row][$i]] = 1;
				}
			}
			
			// Check quadrant of board[row][col]
			$quadrant_row = 1;
			$quadrant_col = 1;
			
			if($row<3){	$quadrant_row = 0;	}
			if($row>5){ $quadrant_row = 2;  }
			$quadrant_row *= 3;
			
			if($col<3){ $quadrant_col = 0;	}
			if($col>5){ $quadrant_col = 2;	}
			$quadrant_col *= 3;
			
			for($i = $quadrant_row; $i<$quadrant_row+3;$i++){
				for($j = $quadrant_col;$j<$quadrant_col+3;$j++){
					if($board[$i][$j] != 0 ){
						$used_values[$board[$i][$j]]=1;
					}
				}
			}
			
			$result = array();
			for($i=1;$i<10;$i++){
				if($used_values[$i]==0){
					array_push($result,$i);
				}
			}
			
			return $result;
		}


		function solve($board){
			$blank_row=-1;
			$blank_col=-1;

			for($i=0;$i<9;$i++){
				for($j=0;$j<9;$j++){
					if($board[$i][$j]==0){
						$blank_row = $i;
						$blank_col = $j;
						break;
					}
				}
				
				if($blank_row != -1){
					break;
				}
			}
			
			if($blank_row==-1){
				if($this->do_print){
					print "Solution:\n";
					$this->print__board($board);
				}
				$this->write_board($board);
				return true;
			}

			$allowed_values = $this->possible_values($board,$blank_row,$blank_col);

			for($i=0;$i<sizeof($allowed_values);$i++){
				$board[$blank_row][$blank_col] = $allowed_values[$i];
				if($this->solve($board)){
					return true;
				}
			}

			return false;
		}


		// returns a 9x9 grid of arrays of possible legal values
		// of each cell of the given board
		function cell_values($board){
			$cells = array_pad(array(),9,array());

			for($i=0;$i<9;$i++){
				for($j=0;$j<9;$j++){
					if($board[$i][$j]==0){
						$cells[$i][$j] = $this->possible_values($board,$i,$j);
					}
					else{
						$cells[$i][$j] = array();
					}
				}
			}

			return $cells;
		}


		/// If we look at the empty cells of a column or row and there
		/// is only one cell that can fit a certain value for that
		/// column, then that cell should have that value.
		function fill_hidden_singles($board){
			$cells = $this->cell_values($board);

			// First fill all hidden singles per column
			$cell_changed = true;
			while($cell_changed){
				$cell_changed = false;
				for($i = 0; $i<9;$i++){
					$count_encounters = array_pad(array(),10,0);
					for($j=0;$j<9;$j++){
						for($k=0;$k<count($cells[$j][$i]);$k++){
							$count_encounters[$cells[$j][$i][$k]]++;
						}
					}
	
					$hidden_singles = array();
					for($j=0;$j<10;$j++){
						if($count_encounters[$j]==1){
							array_push($hidden_singles,$j);
						}
					}
	
					foreach($hidden_singles as $value){
						for($j=0;$j<9;$j++){
							if(in_array($value,$cells[$j][$i])){
								$board[$j][$i] = $value;
								$cells = $this->cell_values($board);
								$cell_changed = true;
							}
						}
					}
				}
			}

			// Fill all hidden singles per row
			$cell_changed = true;
			while($cell_changed){
				$cell_changed = false;
				for($j = 0; $j<9;$j++){
					$count_encounters = array_pad(array(),10,0);
					for($i=0;$i<9;$i++){
						for($k=0;$k<count($cells[$j][$i]);$k++){
							$count_encounters[$cells[$j][$i][$k]]++;
						}
					}
	
					$hidden_singles = array();
					for($i=0;$i<10;$i++){
						if($count_encounters[$i]==1){
							array_push($hidden_singles,$i);
						}
					}
	
					foreach($hidden_singles as $value){
						for($i=0;$i<9;$i++){
							if(in_array($value,$cells[$j][$i])){
								$board[$j][$i] = $value;
								$cells = $this->cell_values($board);
								$cell_changed = true;
							}
						}
					}
				}
			}

			return $board;
		}


		function smart_solve($board){
			$board = $this->fill_hidden_singles($board);
			$this->solve($board);
		}


		function solve_board(){
			$this->smart_solve($this->board);
		}
	}
	
	$sudoku = new Sudoku($argv[1]);

	if(sizeof($argv)==3 && $argv[2]=="-p"){
		$sudoku->set_print(true);
		print "Input:\n";
		$sudoku->print_board();
		print "\n";
	}
	//$board->print_board();
	$sudoku->solve_board();
	//$board->write_board();
	
	
	/*
	Idea:
	solve:
		| board has blanks? : print, write, return true;
		| find first blank
		| make array of possible values for blank
		| if array is empty return false
		| set blank as first value of the array
		| call solve with altered board 
		| if call returns true: solved 
		| check for next number in array of
		| if none work return false

	smart solve:
		| fill in all hidden singles per row and column
		| call solve
	
		This is needed because the recursive function nearly
	chokes to death and takes about a minute to solve a 17
	clue sudoku (board 4 or board 6)
	*/
?> 