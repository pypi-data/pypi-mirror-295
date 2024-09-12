use colored::{ColoredString, Colorize};
use pyo3::prelude::*;
use rand::Rng;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

/// A Python module implemented in Rust.
#[pymodule]
fn c2048(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_class::<Tile>()?;
    m.add_class::<Move>()?;
    m.add_class::<C2048>()?;
    m.add_class::<Energy>()?;
    m.add_class::<FullEnergy>()?;
    Ok(())
}
use std::{
    fmt::{Display, Write},
    ops::AddAssign,
};

const L: usize = 4;

#[pyclass(eq, ord, get_all)]
#[derive(Debug, Default, Clone, PartialEq, Eq, PartialOrd, Ord)]
pub struct Tile {
    pub exp: usize,
    pub is_merged: bool,
}

#[pymethods]
impl Tile {
    #[new]
    pub fn new(exp: usize) -> Self {
        Self {
            exp,
            is_merged: false,
        }
    }

    pub fn to_number(&self) -> usize {
        1 << self.exp
    }

    #[allow(clippy::inherent_to_string)]
    pub fn to_string(&self) -> String {
        match self.exp {
            0 => String::new(),
            _ => format!("{}", 1 << self.exp),
        }
    }
}

/// This shouldn't be passed to the python interpreter because I say so
impl Tile {
    pub fn colored(&self) -> ColoredString {
        let i = self.exp;
        match i {
            0 => String::new().on_truecolor(0xEE, 0xEE, 0xEE),
            1 => self
                .to_string()
                .on_truecolor(0xEE, 0xE4, 0xDA)
                .truecolor(0x12, 0x1A, 0x16),
            2 => self
                .to_string()
                .on_truecolor(0xED, 0xE0, 0xC8)
                .truecolor(0x12, 0x1A, 0x16),
            3 => self
                .to_string()
                .on_truecolor(0xF2, 0xB1, 0x79)
                .truecolor(0xF9, 0xF6, 0xF2),
            4 => self
                .to_string()
                .on_truecolor(0xF5, 0x95, 0x63)
                .truecolor(0xF9, 0xF6, 0xF2),
            5 => self
                .to_string()
                .on_truecolor(0xF6, 0x7C, 0x5F)
                .truecolor(0xF9, 0xF6, 0xF2),
            6 => self
                .to_string()
                .on_truecolor(0xF6, 0x5E, 0x3B)
                .truecolor(0xF9, 0xF6, 0xF2),
            7 => self
                .to_string()
                .on_truecolor(0xED, 0xDF, 0x72)
                .truecolor(0xF9, 0xF6, 0xF2),
            8 => self
                .to_string()
                .on_truecolor(0xED, 0xCC, 0x61)
                .truecolor(0xF9, 0xF6, 0xF2),
            9 => self
                .to_string()
                .on_truecolor(0xED, 0xC8, 0x50)
                .truecolor(0xF9, 0xF6, 0xF2),
            10 => self
                .to_string()
                .on_truecolor(0xED, 0xC5, 0x3F)
                .truecolor(0xF9, 0xF6, 0xF2),
            11 => self
                .to_string()
                .on_truecolor(0xED, 0xC2, 0x2E)
                .truecolor(0xF9, 0xF6, 0xF2),
            _ => String::new()
                .on_truecolor(0x3C, 0x3A, 0x32)
                .truecolor(0xF9, 0xF6, 0xF2),
        }
    }
}

#[pyclass(eq, eq_int)]
#[derive(Debug, Clone, PartialEq)]
pub enum Move {
    Up,
    Right,
    Down,
    Left,
}

#[pymethods]
impl Move {
    #[staticmethod]
    pub fn random() -> Self {
        let i = rand::thread_rng().gen_range(0..L);
        match i {
            0 => Move::Up,
            1 => Move::Right,
            2 => Move::Down,
            _ => Move::Left,
        }
    }
}

#[pyclass(eq, get_all)]
#[derive(Debug, Default, Clone, PartialEq)]
pub struct C2048 {
    pub grid: [Tile; 16],
    pub moves: Vec<Move>,
    pub spawns: Vec<(usize, usize)>,
    pub has_moved: bool,
}

#[pymethods]
impl C2048 {
    #[new]
    pub fn new() -> Self {
        let mut c2048 = C2048::default();
        c2048.spawn_tile(1.0);
        c2048.spawn_tile(1.0);
        c2048
    }

    pub fn __repr__(&self) -> String {
        format!("{self}")
    }

    pub fn spawn_tile(&mut self, chance: f64) {
        let mut rng = rand::thread_rng();
        let value = if rng.gen_bool(chance) { 1 } else { 2 };

        loop {
            let i = rng.gen_range(0..16);

            if self.grid[i].exp == 0 {
                self.set_tile(i, value);
                self.spawns.push((i, value));
                break;
            }
        }
    }

    pub fn has_space(&self) -> bool {
        self.grid.iter().any(|t| t.exp == 0)
    }

    pub fn set_tile(&mut self, pos: usize, value: usize) {
        self.grid[pos].exp = value;
    }

    pub fn highest(&self) -> usize {
        1 << self.grid.iter().max().unwrap().exp
    }

    pub fn score(&self) -> usize {
        self.grid.iter().map(|t| 1 << t.exp).sum()
    }

    pub fn is_lose(&self) -> bool {
        if self.grid.iter().any(|i| i.exp == 0) {
            return false;
        }
        for x in 0..L - 1 {
            for y in 0..L - 1 {
                let i = x + y * L;
                if self.grid[i] == self.grid[i + 1] || self.grid[i] == self.grid[i + L] {
                    return false;
                }
                let i = L - 1 + y * L;
                if self.grid[i] == self.grid[i + L] {
                    return false;
                }
                let i = x + (L - 1) * L;
                if self.grid[i] == self.grid[i + 1] {
                    return false;
                }
            }
        }
        true
    }

    pub fn is_win(&self) -> bool {
        self.grid.iter().any(|t| t.exp >= 11)
    }

    pub fn reset(&mut self) {
        for tile in self.grid.iter_mut() {
            tile.is_merged = false;
        }
        self.has_moved = false;
    }

    pub fn r#move(&mut self, mv: Move) {
        match mv {
            Move::Up => self.up(),
            Move::Right => self.right(),
            Move::Down => self.down(),
            Move::Left => self.left(),
        }
        if self.has_moved {
            self.moves.push(mv);
        }
    }

    pub fn clone_move(&self, mv: Move) -> Self {
        let mut clone = self.clone();
        clone.r#move(mv);
        clone
    }

    pub fn lowest_energy_move(&self) -> Self {
        let up = self.clone_move(Move::Up);
        let right = self.clone_move(Move::Right);
        let down = self.clone_move(Move::Down);
        let left = self.clone_move(Move::Left);
        let moves = vec![up, right, down, left];
        let min = moves
            .into_iter()
            .filter(|g| g.has_moved)
            .min_by_key(|g| g.energy());
        min.unwrap_or(self.clone())
    }

    pub fn left(&mut self) {
        for y in 0..L {
            for x in 1..L {
                let i = x + y * L;
                if self.grid[i].exp == 0 {
                    continue;
                }

                for c in 0..x {
                    let from = i - c;
                    let to = i - c - 1;
                    avance!(self, from, to);
                }
            }
        }
    }

    pub fn right(&mut self) {
        for y in 0..L {
            for x in (0..L - 1).rev() {
                let i = x + y * L;
                if self.grid[i].exp == 0 {
                    continue;
                }

                for c in 0..=2 - x {
                    let from = i + c;
                    let to = i + c + 1;
                    avance!(self, from, to);
                }
            }
        }
    }

    pub fn up(&mut self) {
        for x in 0..L {
            for y in (0..L - 1).rev() {
                let i = x + y * L;
                if self.grid[i].exp == 0 {
                    continue;
                }

                for c in 0..=2 - y {
                    let from = i + c * L;
                    let to = i + (c + 1) * L;
                    avance!(self, from, to);
                }
            }
        }
    }

    pub fn down(&mut self) {
        for x in 0..L {
            for y in 1..L {
                let i = x + y * L;
                if self.grid[i].exp == 0 {
                    continue;
                }

                for c in 0..y {
                    let from = i - c * L;
                    let to = i - (c + 1) * L;
                    avance!(self, from, to);
                }
            }
        }
    }

    pub fn energy(&self) -> isize {
        let mut energy = Energy::default();
        for x in 0..L {
            for y in 0..L {
                let i = x + y * L;
                energy += self.full_energy_at(i).reduce();
            }
        }
        energy.sum()
    }

    pub fn full_energy_at(&self, i: usize) -> FullEnergy {
        let mut e = FullEnergy::default();
        let exp = self.grid[i].exp;
        if exp == 0 {
            e.epsilon = -1;
            return e;
        } else {
            e.epsilon = exp as isize;
        }
        let iexp = exp as isize;

        let x = i % L;
        let y = i / L;
        let right = if x + 1 < L {
            Some(&self.grid[i + 1])
        } else {
            None
        };
        let left = if x > 0 { Some(&self.grid[i - 1]) } else { None };
        let up = if y + 1 < L {
            Some(&self.grid[i + L])
        } else {
            None
        };
        let down = if y > 0 { Some(&self.grid[i - L]) } else { None };

        if let Some(left) = left {
            if left.exp == exp {
                e.phi_left = Some(-iexp);
            } else {
                e.phi_left = Some(iexp);
            }
        }
        if let Some(right) = right {
            if right.exp == exp {
                e.phi_right = Some(-iexp);
            } else {
                e.phi_right = Some(iexp);
            }
        }
        if let Some(up) = up {
            if up.exp == exp {
                e.phi_up = Some(-iexp);
            } else {
                e.phi_up = Some(iexp);
            }
        }
        if let Some(down) = down {
            if down.exp == exp {
                e.phi_down = Some(-iexp);
            } else {
                e.phi_down = Some(iexp);
            }
        }

        if let (Some(up), Some(down)) = (up, down) {
            let up = up.exp;
            let down = down.exp;

            if (up == exp + 1 && down == exp - 1) || (up == exp - 1 && down == exp + 1) {
                e.xi_vertical = Some(-iexp);
            } else {
                e.xi_vertical = Some(iexp);
            }
        }

        if let (Some(left), Some(right)) = (left, right) {
            let left = left.exp;
            let right = right.exp;

            if (left == exp + 1 && right == exp - 1) || (left == exp - 1 && right == exp + 1) {
                e.xi_horizontal = Some(-iexp);
            } else {
                e.xi_horizontal = Some(iexp);
            }
        }

        e
    }
}

#[macro_export]
macro_rules! avance {
    ($self:tt, $from:tt, $to:tt) => {
        if ($self.grid[$to].exp == $self.grid[$from].exp
            && (!$self.grid[$to].is_merged && !$self.grid[$from].is_merged))
        {
            $self.grid[$to].exp += 1;
            $self.grid[$from].exp = 0;
            $self.grid[$to].is_merged = true;
            $self.has_moved = true;
        } else if ($self.grid[$to].exp == 0) {
            $self.grid[$to].exp = $self.grid[$from].exp;
            $self.grid[$to].is_merged = $self.grid[$from].is_merged;
            $self.grid[$from].exp = 0;
            $self.grid[$from].is_merged = false;
            $self.has_moved = true;
        } else {
            break;
        }
    };
}

impl Display for C2048 {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        for y in (0..L).rev() {
            for x in 0..L {
                f.write_str(format!("{: >4} ", self.grid[x + y * L].colored()).as_str())?;
            }
            f.write_char('\n')?;
        }
        Ok(())
    }
}

#[pyclass(eq, get_all)]
#[derive(Debug, Default, PartialEq)]
pub struct FullEnergy {
    epsilon: isize,
    phi_up: Option<isize>,
    phi_down: Option<isize>,
    phi_left: Option<isize>,
    phi_right: Option<isize>,
    xi_vertical: Option<isize>,
    xi_horizontal: Option<isize>,
}

#[pymethods]
impl FullEnergy {
    pub fn reduce(&self) -> Energy {
        Energy {
            epsilon: self.epsilon,
            phi: self.phi_down.unwrap_or_default()
                + self.phi_up.unwrap_or_default()
                + self.phi_left.unwrap_or_default()
                + self.phi_right.unwrap_or_default(),
            xi: self.xi_horizontal.unwrap_or_default() + self.xi_vertical.unwrap_or_default(),
        }
    }
}

#[pyclass(eq, get_all)]
#[derive(Debug, Default, PartialEq)]
pub struct Energy {
    epsilon: isize,
    phi: isize,
    xi: isize,
}

#[pymethods]
impl Energy {
    pub fn sum(&self) -> isize {
        self.epsilon + self.phi + self.xi
    }
}

impl AddAssign for Energy {
    fn add_assign(&mut self, rhs: Self) {
        self.epsilon += rhs.epsilon;
        self.phi += rhs.phi;
        self.xi += rhs.xi;
    }
}
