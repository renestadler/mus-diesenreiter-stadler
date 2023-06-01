package at.fhooe.recyclingserver.controller;

import at.fhooe.recyclingserver.logic.ProductLogic;
import at.fhooe.recyclingserver.model.Product;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import static java.util.Objects.requireNonNull;

@RestController
public class ProductController {

    private static final Logger LOG = LoggerFactory.getLogger(ProductController.class);
    private final ProductLogic productLogic;

    public ProductController(ProductLogic productLogic) {
        this.productLogic = requireNonNull(productLogic);
    }

    @GetMapping("/product")
    public ResponseEntity<Product> getProduct(@RequestParam("barcode") String code) {

        LOG.info("Getting product for barcode {}", code);
        return ResponseEntity.of(productLogic.getProduct(code));
    }
}
