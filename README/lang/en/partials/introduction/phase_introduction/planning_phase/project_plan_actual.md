
### **Introduction / Phase Introduction / Planning Phase / Project Plan**

Decide on the encoding sets and supported language scripts. Decide and plan the weights and how you will generate each weight. Understand the procedures and steps. Calculate or keep track of timelines, steps procedures and pitfalls.

1.  **Project Plan** Components ∞0.001:
	1.  **Design**
	1.  **Production**
	1.  **Alteration Functions**

---

### **Introduction / Phase Introduction / Planning Phase / Project Plan / Design**

BUMP

---

### **Introduction / Phase Introduction / Planning Phase / Project Plan / Production**

BUMP


---

### **Introduction / Phase Introduction / Planning Phase / Project Plan / Syntax**


*  The selector represents to the letter you want to create and the attribute in the square brackets represents the source of that letter.

*  The declaration block contains one or more declarations separated by semicolons.

*  Each declaration includes a SYFF property name and a value, separated by a colon.

*  Multiple SYFF declarations are separated with semicolons, and declaration blocks are surrounded by curly braces.

*  SYFF selectors outside of Instance Queries, apply to all the instances of a given font. Selectors inside Instance Queries apply to specific instances of the font, like Media Queries with devices or sizes.



---

### **Introduction / Phase Introduction / Planning Phase / Project Plan / Syntax / Blocks**



#### Initial Letter Definitions:


```css

Π {

	out: "P_i";

}


```


#### Synthesized Letter Definitions:



```css

/* produced (character) [ receiving (character) = "name, unicode" ] */

Ш [ Π = "uni0428, 0428" ] {

	transform: fontex("width","right", 100, 0);
	transform: mirrorX();

}


```

---

### **Introduction / Phase Introduction / Planning Phase / Project Plan / Syntax / Instance Query**

SYFF selectors outside of Instance Queries, apply to all the instances of a given font. Selectors inside Instance Queries apply to specific instances of the font, like Media Queries and devices or sizes.


<br>

```css

/* Define the existing letter */

A {

	out: "A_lpha";

}


/* Translate -50 for all instances */

Α [ A = "Alpha, 0391" ] {

	transform: translate(-50, 0);

}


@instance ("bold") {

	/* Translate another -20 for only bold instance */

    Α [ A = "Alpha, 0391" ] {

		transform: translate(-20, 0);

	}

}


```


---


### **Introduction / Phase Introduction / Planning Phase / Project Plan / Alteration Functions**


Review and document the Alteration Functions:

*	[Copy](https://github.com/VivaRado/SYFF#copy)
*	[Transform](https://github.com/VivaRado/SYFF#translate)
*	[Mirror](https://github.com/VivaRado/SYFF#mirror)
*	[Fontex](https://github.com/VivaRado/SYFF#fontex)
*	[Partial](https://github.com/VivaRado/SYFF#partial)
* Logging


---


### **Introduction / Phase Introduction / Planning Phase / Project Plan / Alteration Functions / Copy**

The definition of a SYFF rule is a copy function.


<br>

```css

A [ B = "name, unicode" ] {}


```

<br>

---

### **Introduction / Phase Introduction / Planning Phase / Project Plan / Alteration Functions / Translate**

Translate a partial or the whole letter.

<br>

```css

A [ B = "name, unicode" ] {

	transform: translate("partial_name", X, Y);
	transform: translate(X, Y);

}


```

<br>

#### Transform Translate Function:

```css
transform: translate("partial_name", X, Y);
transform: translate(X, Y);

<transform()> = translate( <partial-name-string>?, <number>, <number>  )

```

---

### **Introduction / Phase Introduction / Planning Phase / Project Plan / Alteration Functions / Mirror**

Mirror a partial or the whole letter.

<br>

```css

A [ B = "name, unicode" ] {

	transform: mirrorX();
	transform: mirrorX( "hand_copy" );
	transform: mirrorY();
	transform: mirrorY( "hand_copy" );

}


```
<br>

#### Transform Mirror Function:

```css
transform: mirrorX();
transform: mirrorY("hand_copy");

<transform()> = mirrorX( <partial-name-string>? )
<transform()> = mirrorY( <partial-name-string>? )

```

<br>

---

### **Introduction / Phase Introduction / Planning Phase / Project Plan / Alteration Functions / Fontex**

Fontex is defined as an instance like all the rest of the instances of your font, but it includes areas, instead of letters, defined by you for specific purposes.


<br>

<div markdown='1' class="img_narrow">

![Screenshot](assets/media/P_i_fontex.svg)

</div>

<br>

Here we can translate the points in the left width region.

<br>

<div markdown='1' class="img_narrow">

![Screenshot](assets/media/P_i_fontex_translate.svg)

</div>


<br>

```css

A [ B = "name, unicode" ] {

	transform: fontex("type","position", X, Y);

}

```
<br>


#### Transform Fontex Function:

```css
transform: fontex("type","position", X, Y);

<transform()> = fontex( <type-string>, <position-string>, <number>, <number> )

```

<br>

Here is a GLIF with some areas defined by fontex, using these areas we can then manipulate the included points. Since fontex is tied to the first instance of your font, and we are dealing with a variable font, those points are at the same index and same partial across all other instances too.

We can then use these fontex to move points and make letters wider or other detailing.

<br>

```xml

<?xml version="1.0" encoding="UTF-8"?>
<glyph name="Pi" format="1">
  <advance width="679"/>
  <unicode hex="03A0"/>
  <outline>
    <contour>
      <point x="-25" y="-20" type="line" name="{type:width,position:left}"/>
      <point x="152" y="-20" type="line" />
      <point x="152" y="674" type="line" />
      <point x="-25" y="674" type="line" />
    </contour>
    <contour>
      <point x="385" y="-20" type="line" name="{type:width,position:right}"/>
      <point x="562" y="-20" type="line" />
      <point x="562" y="674" type="line" />
      <point x="385" y="674" type="line" />
    </contour>
  </outline>
</glyph>


```

---

### **Introduction / Phase Introduction / Planning Phase / Project Plan / Alteration Functions / Partial**

You can divide your letter in partials which you can use across your other letters, you could also make one letter that includes all the partials you will need and then run the appropriate SYFF functions to create the whole font.

<br>

```css

A [ B = "name, unicode" ] {

	partial: keep("partial_a", "partial_b");
	partial: remove("partial_b");
	partial: get("Π","partial_a", "partial_a_rename");
	partial: copy("partial_a", "partial_a_rename");

}


```

<br>

#### Partial Keep Function:

```css
partial: keep("partial_a", "partial_b");

<partial()> = keep( [<partial-name-string> , <partial-name-string>, ...] )

```

#### Partial Remove Function:

```css
partial: remove("partial_b");

<partial()> = remove( [<partial-name-string> , <partial-name-string>, ...] )

```

#### Partial Get Function:

```css
partial: get("Π","partial_a","partial_a_rename");

<partial()> = get( <letter-name-string> , <partial-name-string>, <partial-new-name-string> )

```

#### Partial Copy Function:

```css
partial: copy("partial_a");
partial: copy("partial_a", "partial_a_rename");

<partial()> = copy( <partial-name-string>, <partial-new-name-string>? )

<partial-new-name-string> = <string>.<int>


```

<br>


---

### **Introduction / Phase Introduction / Planning Phase / Project Plan / Alteration Functions / Logging**

A basic log function should exist to cover some of the alteration functions.


<br>

```css

A [ B = "name, unicode" ] {

  log: /* In Planning */;

}


```

<br>

#### Logging Function:

```css
log: /* In Planning */;

<log()> = function( <string> , <string>? )

```

---

### **Introduction / Phase Introduction / Planning Phase / Project Plan / Examples**

#### E to F to Γ to T 

Here is an example of the letter E becoming F, then Γ and T. The first point of each part of this letter have a piece of code in the name definition that allows us access with SYFF.

<br>

```fontex
{type:part,position:hand}

```

<br>


<br>

<div markdown='1' class="img_narrow">

![Screenshot](assets/media/E_psilon_demo.svg)

</div>


```css

Ε {

	out: "E_psilon";

}

/* We create a new letter out of the Epsilon glyph */

E [ Ε = "E, 0045" ] {}

/* 
We create a new letter F and then use the partial function, 
by keeping and removing the curved "leg" partial,
we need a new straight leg - stem for F and we can grab that from the letter I
*/

F [ E = "F, 0046" ] { 

	partial: keep("hand","arm","tie","leg"); /* Demonstrating Partial Keep and Remove */
	partial: remove("leg");
	partial: get("I","leg","leg_new"); /* get and rename */

}

/* 
We create a new letter Γ (Gamma) and then use the partial function and removing the "tie" partial.
*/

Γ [ F = "Gamma, 0393" ] { 

	partial: remove("tie");

}

/* 
We create a new letter Τ (Tau) and then use the partial function and removing the "arm" partial, 
then we copy the "hand" partial which gives us "hand_copy" (or hand_001 subject to change), 
finally we mirror "hand_copy" and translate it -100 on the X axis.
*/

Τ [ Γ = "Tau, 03A4" ] { 

	partial: remove("arm");
	partial: copy("hand", "hand_copy");
	transform: mirrorY( "hand_copy" );
	transform: translate("hand_copy", -100, 0);

}

/*
And here is a copy of Tau to create T
*/

Τ [ T = "T, 0054" ] {}



```

<br>

The glif in question:

<br>


```xml

<?xml version="1.0" encoding="UTF-8"?>
<glyph name="Epsilon" format="1">
  <advance width="415"/>
  <unicode hex="0395"/>
  <outline>
    <contour>
      <point x="115" y="559" type="line" name="{type:part,position:hand}"/>
      <point x="115" y="650" type="line"/>
      <point x="415" y="650" type="line"/>
      <point x="415" y="580" type="line"/>
      <point x="360" y="559" type="line"/>
    </contour>
    <contour>
      <point x="0" y="338" type="line" name="{type:part,position:arm}"/>
      <point x="0" y="579" type="line"/>
      <point x="64" y="650" type="line"/>
      <point x="119" y="650" type="line"/>
      <point x="119" y="559" type="line"/>
      <point x="105" y="559" type="line"/>
      <point x="91" y="544" type="line"/>
      <point x="91" y="338" type="line"/>
    </contour>
    <contour>
      <point x="278" y="293" type="line" name="{type:part,position:tie}"/>
      <point x="67.6692" y="292.585" type="line"/>
      <point x="67.6692" y="383.588" type="line"/>
      <point x="320.628" y="383.715" type="line"/>
      <point x="320.628" y="336" type="line"/>
    </contour>
    <contour>
      <point x="91" y="342" type="line" name="{type:part,position:leg}"/>
      <point x="91" y="106" type="line"/>
      <point x="105" y="91" type="line"/>
      <point x="119" y="91" type="line"/>
      <point x="119" y="0" type="line"/>
      <point x="64" y="0" type="line"/>
      <point x="0" y="71" type="line"/>
      <point x="0" y="342" type="line"/>
    </contour>
    <contour>
      <point x="115" y="0" type="line" name="{type:part,position:foot}"/>
      <point x="115" y="91" type="line"/>
      <point x="360" y="91" type="line"/>
      <point x="415" y="70" type="line"/>
      <point x="415" y="0" type="line"/>
    </contour>
  </outline>
</glyph>


```

---


### **Introduction / Phase Introduction / Planning Phase / Project Plan / Delivery**

SYFF will be delivered in this repository.

---

### **Introduction / Phase Introduction / Planning Phase / Project Plan / Usage**


####  **To apply the SYFF:**

Planned:

```python3 '/syff.py' -s '/font.designspace' -c '/font.syff' --output-path '/adventpro-VF.ufo'```

---

Current Test:

```python3 '/syff.py' -s '/demo.syff'```

