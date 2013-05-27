input = Dir["data/in.*"]

# ./bin/trix  -a search data/exampleinput.txt data/out

Dir["data/in.*"].each do |file|
  out_file = file.gsub("/in.", "/out.")
  puts "Generating: #{file} => #{out_file}"
  system "./bin/trix", "-a", "search", file, out_file
  puts "Done."
end