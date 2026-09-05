---
part: Two — The Settled Question
chapter: 6
title: Safe, According to the Model
---

# Chapter 6 — Safe, According to the Model

An engineer's confidence is different from a scientist's, because it is written down as a number and somebody's life is resting on it.

That ought to make it more reliable, and mostly it does. The buildings stand up. What this chapter collects is the small proportion of cases where the number was produced correctly by a method that had quietly stopped describing the thing being built. The arithmetic looks identical either way. A calculation cannot tell you that it is answering the wrong question.

Three failures recur. The first is the untested extrapolation. A design method that has worked for twenty structures is applied to one that is longer, thinner, faster or deeper than any of them. The range over which it was validated goes unmentioned, because everyone has forgotten there was one. The second is the missing failure mode, where every load anybody thought of was analysed properly and the one that killed it was not on the list. The third is organisational, and it is the worst: the number was right, somebody said so, and the structure was built anyway.

Notice how many of these had a warning. Not a vague misgiving afterwards, but a specific person saying a specific thing beforehand, in writing, and being overruled or ignored. That pattern is so consistent it is nearly a law, and it is the strongest practical argument in this book. If you want to know whether your project is about to fail, the useful question is not whether you are confident. It is who has already told you it will, and what happened to them. The shape is the same in a warship of 1628 and a submersible of 2023: somebody measured the thing, somebody said out loud what the measurement meant, and the decision was taken by a person for whom stopping had become more expensive than continuing.

---

> **The ship is stable enough. Sail her.** — Gustavus Adolphus, 1628

**What happened.** She sank in the harbour. The Vasa was the most powerful warship in the Baltic, built in haste for a war, with a second gun deck added at the king's request while she was on the stocks. Before launch the shipyard ran a stability test in which thirty men ran from side to side across the deck; it was stopped after three passes because the ship was rolling dangerously. She sailed on 10 August 1628, caught a gust in Stockholm harbour, heeled over, took water through the open lower gunports and sank about 1,300 metres into her maiden voyage. The inquiry found nobody at fault. She was raised in 1961 and is intact.

**What the error was made of.** A test that was performed, understood and then not allowed to mean anything. This is the purest version of the pattern in this chapter: nobody lacked the information. The men on the deck knew, and so did the officer who stopped the test. The knowledge did not travel upwards, because the man it had to reach had already decided and was at war. Every subsequent entry here is a more sophisticated version of the same thirty men running from side to side.

---

> "The captain can, by simply moving an electric switch, instantly close the doors throughout, practically making the vessel unsinkable." — The Shipbuilder, 1911

**What happened.** One year. The Titanic's hull was divided into sixteen watertight compartments and could float with any two of them flooded, or with the first four. The iceberg opened six. She sank on 15 April 1912 with about 1,500 people aboard, having carried lifeboats for roughly half those on board, which was more than the regulations of the day required.

**What the error was made of.** A design case treated as a guarantee. The compartment system was real, it was well engineered, and the phrase in the trade press was hedged with the word *practically*, which everybody dropped. The failure is worth stating plainly, because it repeats. The ship was designed against the worst accident anyone had seen, which was a collision at a bulkhead. The sea is not obliged to stay inside the range of your experience. The lifeboats are the more damning half. They were adequate for the ship in the model and not for the ship that existed.

---

> **The deflection theory permits a far lighter and shallower deck than earlier practice, at no cost in safety.** — Leon Moisseiff, 1940

**What happened.** Four months. The Tacoma Narrows Bridge opened in July 1940 with a deck eight feet deep on a span of over eight hundred metres, the most slender suspension bridge ever built. It moved in light winds from the first day and was nicknamed Galloping Gertie by the people who drove over it. On 7 November, in a wind of about forty miles an hour, well below its design load, it went into a twisting oscillation and tore itself apart. The film of it is the most-watched engineering failure in history.

**What the error was made of.** A method extrapolated past the conditions that validated it. Moisseiff's theory was sound and had produced excellent bridges; it treated wind as a static horizontal force, which is adequate for a stiff deck and catastrophic for a flexible one. Aerodynamic flutter was not a phenomenon suspension bridge engineers had needed to think about, because no previous deck had been light enough to flutter. Every design method has a range of validity, and the range is invisible from inside it until something leaves it.

---

> **The pressurised cabin is amply strong. The airframe is good for tens of thousands of cycles.** — de Havilland, 1952

**What happened.** Three broke up in the air. The Comet was the first jet airliner and a genuine triumph, in service in May 1952 and a year ahead of anything else in the world. Three broke up in flight within twenty-six months. The investigation submerged an entire fuselage in a water tank and pressurised it thousands of times. It found metal fatigue starting at the corners of cutouts in the skin, where the stress concentrated far more than the calculations assumed. The design was corrected, the type flew safely for decades afterwards, and Boeing and Douglas took the market.

**What the error was made of.** A material behaviour that had not mattered before and did now. Fatigue was known. What was new was a pressurised cabin cycled twice a day behind a thin skin at high altitude, and the safety factor that covered every previous aircraft did not cover it. The reason this entry is here rather than in a chapter about ordinary bad luck is the water tank: the test that found the answer was not exotic, and it existed. It was simply not thought necessary until after the crashes.

---

> **The walkway connection as fabricated is equivalent to the design.** — The Hyatt Regency engineers, 1979

**What happened.** Two years. Two suspended walkways in the atrium of the Kansas City hotel were to hang from single continuous rods. During fabrication the detail was changed to two shorter rods, with the upper walkway hanging from the lower one's box beam, because a continuous threaded rod is awkward to make and install. The change doubled the load on that connection. On 17 July 1981, during a crowded tea dance, both walkways came down. A hundred and fourteen people died. It remains one of the worst structural failures in American history, and both engineers lost their licences.

**What the error was made of.** A change nobody costed because it looked like a detail. The original design was already marginal, which is the part usually left out, and the modification turned marginal into fatal. What makes it the standard teaching case is how ordinary the failure is. A fabricator proposed a simpler way to build a joint. A shop drawing came back and somebody approved it under time pressure without redoing the arithmetic, and the arithmetic was five minutes of work. Almost nothing here required expertise. It required somebody to treat a small change as a change.

---

> "A reactor of this type could be installed on Red Square. It is no more dangerous than a samovar." — attributed to Anatoly Aleksandrov, 1980

**What happened.** Unit 4 exploded. Aleksandrov was president of the Soviet Academy of Sciences and one of the fathers of the RBMK design. The reactor had a positive void coefficient, meaning that in certain conditions a loss of cooling increases the reaction rather than damping it, and control rods that briefly added reactivity as they entered. Both were known to the designers and neither was in the operating manuals at Chernobyl. Unit 4 exploded on 26 April 1986 during a test of the turbine at low power.

**What the error was made of.** A hazard known at the top and absent at the bottom. This is what happens where admitting a defect is politically costly. The information does not disappear. It gets classified, and the people who need it most are cleared least. The operators at Chernobyl did the wrong thing that night, and there is no version of the story in which they could have known why it was wrong. A safety culture is not a set of attitudes. It is a question about who is allowed to know what.

---

> **The probability of a catastrophic failure is about one in a hundred thousand flights.** — NASA management, 1986

**What happened.** Seventy-three seconds. Challenger broke up seventy-three seconds after launch on 28 January 1986, on the twenty-fifth shuttle flight. The night before, engineers at Morton Thiokol had recommended against launching. The O-ring seals in the solid rocket boosters had never been tested near the forecast temperature and had shown erosion on earlier cold flights. They were asked to reconsider as managers rather than as engineers, and the recommendation was reversed. Richard Feynman sat on the commission afterwards. He found that working engineers put the odds of loss at around one in a hundred while management used a figure a thousand times better, and he asked, in the report's appendix, what the basis for it was.

**What the error was made of.** Evidence of a problem reclassified as evidence of margin. The O-rings had been eroding for years without a loss. That record was read as proof that erosion was survivable, and not as a warning that the seal was not doing its job. Once a deviation has occurred a few times with no consequence it stops being a deviation and becomes the expected condition, and the standard quietly moves. Feynman's closing line is the one to keep: for a successful technology, reality must take precedence over public relations, for nature cannot be fooled.

---

> **The design basis tsunami for the site is 5.7 metres. Higher estimates are not sufficiently established to require action.** — TEPCO, 2008

**What happened.** The wave was fifteen metres. An internal study in 2008 concluded that a tsunami of over fifteen metres was possible at Fukushima Daiichi on the basis of historical events, including one in the year 869. It was treated as provisional and passed for further study rather than acted on. On 11 March 2011 the wave reached roughly fourteen to fifteen metres at the site, flooded the emergency generators in the basements, and three reactors melted down. The Diet's independent commission called the accident profoundly man-made.

**What the error was made of.** A conclusion nobody had to reject because it could be kept pending. The finding was made by the company's own people and never overturned. It was held in the queue, because acting on it meant an enormous expense against an event that had not happened in a thousand years. This is not ignorance, and it is far more common. An organisation never has to decide against an inconvenient finding, because indefinite study is available and looks responsible from every angle.

---

> **The negative pressure test result is anomalous but explainable. The well is secure.** — BP and Transocean, 20 April 2010

**What happened.** The well blew out that evening. A test to confirm the Macondo well was sealed produced pressure readings that should not have been possible if the seal were good. The crew debated it for an hour and settled on an explanation involving a bladder effect in the drilling fluid, a phenomenon with no real basis. They proceeded. The well blew out that evening, eleven men died, the rig sank, and around four million barrels of oil went into the Gulf of Mexico over the following three months.

**What the error was made of.** A rescuing explanation invented at the point of decision. The reading was unambiguous and everyone saw it. One interpretation meant stopping, which was expensive and embarrassing forty days behind schedule. The other meant continuing. So the group looked for a reason the instrument might be lying, and found one. A hypothesis produced only in order to permit the action you already wanted is not a hypothesis, and the moment to notice this is when it is being generated, not afterwards.

---

> "At some point safety is just pure waste. I mean, if you just want to be safe, don't get out of bed, don't get in your car, don't do anything." — Stockton Rush, 2019

**What happened.** Four years. Rush's company took paying passengers to the wreck of the Titanic in a submersible with a carbon fibre hull. The material had no service history at that depth and is known to degrade in ways that are hard to inspect. He declined classification by any marine society, arguing publicly that certification stifles innovation. Employees and outside experts wrote to him warning of catastrophic risk; one was dismissed. The vessel imploded in June 2023, killing him and four others.

**What the error was made of.** A true general observation used to dismiss a specific one. It is perfectly correct that safety has diminishing returns and that a fully risk-averse life is not a life. None of it says anything about whether a particular pressure hull will hold at four thousand metres. The move is a common one and worth being able to name: a philosophical point about risk in general, deployed to avoid an engineering point about this object. The warnings he received were not about the value of caution. They were about the hull.
