fn main() { for value in ["",".","0","-3","1","1.6","0,5","0.5","1,234","1.234,56","1 234,56","3e1","NaN","Infinity","abc","−2"] { let accepted = value.is_empty() || value == "." ||
                    value.parse::<f32>().is_ok_and(|number| (0.0..=50.0).contains(&number)); let step = value
                    .trim()
                    .replace(',', ".")
                    .parse::<f64>()
                    .ok()
                    .filter(|value| value.is_finite())
                    .map(|value| value.round().max(1.0) as usize)
                    .unwrap_or(1); println!("{:?}\t{}\t{}",value,accepted,step); } }